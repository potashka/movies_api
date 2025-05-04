from typing import Optional
import psycopg
from src.core import config

pg: Optional[psycopg.AsyncConnection] = None


async def get_pg() -> psycopg.AsyncConnection:
    if pg is None:
        raise RuntimeError("PG disabled in DOCS_ONLY mode")
    return pg


async def open_pg():
    global pg
    pg = await psycopg.AsyncConnection.connect(
        host=config.PG_HOST,
        port=config.PG_PORT,
        dbname=config.PG_DB,
        user=config.PG_USER,
        password=config.PG_PASSWORD,
    )


async def close_pg():
    await pg.close()
