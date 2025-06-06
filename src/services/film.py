from functools import lru_cache
from http import HTTPStatus
from typing import List

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, HTTPException
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Film, ShortFilm

CACHE_TTL = 60 * 5
INDEX = "movies"


class FilmService:
    """Сервис «Фильмы».

    * Достаёт данные из Elasticsearch.
    * Кэширует результат в Redis (`film:<uuid>`).
    * Выдаёт:
        • подробную карточку фильма;
        • список фильмов с пагинацией;
        • результаты полнотекстового поиска.
    """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Film:
        key = f"film:{film_id}"
        cached = await self.redis.get(key)
        if cached:
            return Film.model_validate_json(cached)

        try:
            doc = await self.elastic.get(index=INDEX, id=film_id)
        except NotFoundError:
            raise HTTPException(HTTPStatus.NOT_FOUND, "film not found")

        film = Film(**doc["_source"])
        await self.redis.set(key, film.model_dump_json(), ex=CACHE_TTL)
        return film

    async def list(
        self,
        *,
        sort: str | None,
        genre: str | None,        # genre — название жанра («Action», «Comedy»)
        page_size: int,
        page_number: int,
    ) -> List[ShortFilm]:
        """ES‑запрос со сортировкой и фильтром по названию жанра."""
        must = []
        if genre:
            # фильтрация по точному значению keyword‑поля                # изменено
            must.append({"term": {"genres": genre}})

        body = {
            "query": {"bool": {"must": must}} if must else {"match_all": {}},
            "from": (page_number - 1) * page_size,
            "size": page_size,
        }
        if sort:
            order = "desc" if sort.startswith("-") else "asc"
            body["sort"] = [{sort.lstrip('-'): {"order": order}}]

        resp = await self.elastic.search(index=INDEX, body=body)
        return [ShortFilm(**hit["_source"]) for hit in resp["hits"]["hits"]]

    async def search(
        self, *, query: str, page_size: int, page_number: int
    ) -> List[ShortFilm]:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "title^3",
                        "description",
                        "actors.full_name",
                        "writers.full_name",
                        "directors.full_name",
                    ],
                }
            },
            "from": (page_number - 1) * page_size,
            "size": page_size,
        }
        resp = await self.elastic.search(index=INDEX, body=body)
        return [ShortFilm(**hit["_source"]) for hit in resp["hits"]["hits"]]


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
