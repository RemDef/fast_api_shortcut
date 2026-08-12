import json

from redis.asyncio import Redis


class RedisCacheBackend:
    def __init__(self, redis_url: str, cache_ttl_seconds: int):
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.cache_ttl_seconds = cache_ttl_seconds

    async def set(self, key: str, value: dict, ttl: int | None = None) -> None:
        await self.redis.set(key, json.dumps(value), ex=ttl or self.cache_ttl_seconds)

    async def get(self, key: str) -> dict | None:
        raw = await self.redis.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def delete_pattern(self, pattern: str) -> None:
        async for key in self.redis.scan_iter(match=pattern):
            await self.redis.delete(key)
