from cache.backend import RedisCacheBackend


async def is_rate_limit_allowed(
    cache: RedisCacheBackend,
    key: str,
    *,
    max_requests: int,
    rate_limit_seconds: int,
) -> bool:
    count = await cache.redis.incr(key)
    if count == 1:
        await cache.redis.expire(key, rate_limit_seconds)
    return count <= max_requests
