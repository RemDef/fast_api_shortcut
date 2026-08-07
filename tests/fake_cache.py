import json


class FakeRedis:
    def __init__(self) -> None:
        self._data: dict[str, str] = {}

    async def incr(self, key: str) -> int:
        value = int(self._data.get(key, "0")) + 1
        self._data[key] = str(value)
        return value

    async def expire(self, key: str, seconds: int) -> bool:
        return True


class FakeCacheBackend:
    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self.redis = FakeRedis()

    async def set(self, key: str, value: dict) -> None:
        self._store[key] = json.dumps(value)

    async def get(self, key: str) -> dict | None:
        raw = self._store.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)

    async def delete_pattern(self, pattern: str) -> None:
        prefix = pattern.rstrip("*")
        for key in list(self._store):
            if key.startswith(prefix):
                del self._store[key]
