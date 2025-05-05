import psycopg

from src.core.config import settings

pg: psycopg.AsyncConnection | None = None  # изменено


async def get_pg() -> psycopg.AsyncConnection:
    if pg is None:
        raise RuntimeError("PG disabled in DOCS_ONLY mode")
    return pg


async def open_pg():
    global pg
    pg = await psycopg.AsyncConnection.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        dbname=settings.pg_db,
        user=settings.pg_user,
        password=settings.pg_password,
    )


async def close_pg():
    await pg.close()
