from functools import lru_cache
from http import HTTPStatus
from typing import List

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, HTTPException
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.genre import Genre

CACHE_TTL = 60 * 5
INDEX = "genres"


class GenreService:
    """Сервис «Жанры».

    Предоставляет основные операции:
    получить жанр по UUID,
    отфильтровать по имени,
    отдать весь список с пагинацией.
    Кэширует каждый жанр в Redis (ключ `genre:<uuid>`).
    """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Genre:
        key = f"genre:{genre_id}"                                    # ключ единого формата
        cached = await self.redis.get(key)
        if cached:
            return Genre.model_validate_json(cached)

        try:
            doc = await self.elastic.get(index=INDEX, id=genre_id)
        except NotFoundError:
            raise HTTPException(HTTPStatus.NOT_FOUND, "genre not found")

        genre = Genre(**doc["_source"])
        await self.redis.set(key, genre.model_dump_json(), ex=CACHE_TTL)
        return genre

    async def list(self, *, page_size: int, page_number: int) -> List[Genre]:
        body = {
            "query": {"match_all": {}},
            "sort": [{"name.keyword": {"order": "asc"}}],
            "from": (page_number - 1) * page_size,
            "size": page_size,
        }
        resp = await self.elastic.search(index=INDEX, body=body)
        return [Genre(**hit["_source"]) for hit in resp["hits"]["hits"]]

    async def search(self, *, query: str, page_size: int, page_number: int) -> List[Genre]:
        body = {
            "query": {"match": {"name": {"query": query, "fuzziness": "auto"}}},
            "from": (page_number - 1) * page_size,
            "size": page_size,
        }
        resp = await self.elastic.search(index=INDEX, body=body)
        return [Genre(**hit["_source"]) for hit in resp["hits"]["hits"]]


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
