from redis.asyncio import Redis  # pylint: disable=no-name-in-module,import-error


redis: Redis | None = None


async def get_redis() -> Redis:
    if redis is None:
        raise RuntimeError("Redis disabled in DOCS_ONLY mode")
    return redis
