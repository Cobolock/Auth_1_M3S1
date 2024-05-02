from redis.asyncio import Redis

from auth.core.config import redis_config

redis: Redis = Redis(host=redis_config.host, port=redis_config.port)


async def get_redis() -> Redis:
    return redis
