# src/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from core import config
from db import elastic, redis, pg
from api.v1 import films, genres, persons


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    elastic.es = AsyncElasticsearch(
        hosts=[f"{config.ELASTIC_SCHEMA}{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"]
    )
    await pg.open_pg()

    yield

    await redis.redis.close()
    await elastic.es.close()
    await pg.close_pg()


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,          # ← новый способ
)

# подключаем роутеры
app.include_router(films.router,  prefix="/api/v1/films",  tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
