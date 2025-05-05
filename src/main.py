# src/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from .core.config import settings   # изменено
from .db import elastic, redis, pg
from .api.v1 import films, genres, persons


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекст жизненного цикла (lifespan) приложения FastAPI.

    При обычном запуске (``DOCS_ONLY = False``):

    * **startup**  
      ─ Подключается к Redis (кеш),  
      ─ создаёт асинхронный клиент Elasticsearch,  
      ─ открывает соединение с PostgreSQL (используется для ETL‑проверок).

    * **shutdown**  
      ─ Корректно закрывает все соединения.

    При запуске «только‑доки» (``DOCS_ONLY = True``) весь сетап/тёрдаун
    пропускается, чтобы можно было открыть Swagger‑UI без поднятых сервисов.

    Parameters
    ----------
    app : fastapi.FastAPI
        Экземпляр приложения, автоматически передаваемый FastAPI.

    Yields
    ------
    None
        Управление возвращается FastAPI — после ``yield`` приложение работает.
    """
    if not settings.docs_only:       # изменено
        redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
        elastic.es = AsyncElasticsearch(
            hosts=[f"{settings.elastic_schema}{settings.elastic_host}:{settings.elastic_port}"]
        )
        await pg.open_pg()

    yield

    if not settings.docs_only:       # изменено
        await redis.redis.close()
        await elastic.es.close()
        await pg.close_pg()


app = FastAPI(
    title=settings.project_name,    # изменено
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(films.router,  prefix="/api/v1/films",  tags=["Фильмы"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["Жанры"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["Персоны"])
