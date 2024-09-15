import redis
from redis.asyncio import Redis

from config import app_config, Config


async def get_redis(config: Config = app_config) -> Redis:
    return redis.asyncio.from_url(
        config.redis.dsn,
        decode_responses=True,
    )
