from functools import lru_cache
from http import HTTPStatus
from typing import List

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, HTTPException
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.person import Person

CACHE_TTL = 60 * 5
INDEX = "persons"


class PersonService:
    """Сервис «Персоны».

    Даёт подробные данные по актёрам/режиссёрам/сценаристам,
    включая список фильмов и ролей.
    Результаты кэшируются: `person:<uuid>`.
    """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Person:
        key = f"person:{person_id}"                                 # ключ единого формата
        cached = await self.redis.get(key)
        if cached:
            return Person.model_validate_json(cached)

        try:
            doc = await self.elastic.get(index=INDEX, id=person_id)
        except NotFoundError:
            raise HTTPException(HTTPStatus.NOT_FOUND, "person not found")

        person = Person(**doc["_source"])
        await self.redis.set(key, person.model_dump_json(), ex=CACHE_TTL)
        return person

    async def list(self, *, page_size: int, page_number: int) -> List[Person]:
        body = {
            "query": {"match_all": {}},
            "sort": [{"full_name.keyword": {"order": "asc"}}],
            "from": (page_number - 1) * page_size,
            "size": page_size,
        }
        resp = await self.elastic.search(index=INDEX, body=body)
        return [Person(**hit["_source"]) for hit in resp["hits"]["hits"]]

    async def search(self, *, query: str, page_size: int, page_number: int) -> List[Person]:
        body = {
            "query": {"match": {"full_name": {"query": query, "fuzziness": "auto"}}},
            "from": (page_number - 1) * page_size,
            "size": page_size,
        }
        resp = await self.elastic.search(index=INDEX, body=body)
        return [Person(**hit["_source"]) for hit in resp["hits"]["hits"]]


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
