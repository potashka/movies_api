from typing import Optional
from redis.asyncio import Redis  # pylint: disable=no-name-in-module,import-error


redis: Optional[Redis] = None

async def get_redis() -> Redis:
    return redis
