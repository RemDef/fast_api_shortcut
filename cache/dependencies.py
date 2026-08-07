from cache.backend import RedisCacheBackend
from config import settings

cache_backend = RedisCacheBackend(
    redis_url=settings.redis_url,
    cache_ttl_seconds=settings.cache_ttl_seconds,
)


def get_cache() -> RedisCacheBackend:
    return cache_backend
