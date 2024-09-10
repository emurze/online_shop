import redis
from redis.asyncio import Redis

from config import config


async def get_redis() -> Redis:
    return redis.asyncio.from_url(
        config.redis_dsn,
        decode_responses=True,
    )
