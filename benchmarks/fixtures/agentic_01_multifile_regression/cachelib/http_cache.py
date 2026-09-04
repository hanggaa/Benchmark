from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .cache_control import parse_cache_control


@dataclass
class _Entry:
    value: Any
    expires_at: float
    stale_until: float


class HTTPCache:
    def __init__(self) -> None:
        self._entries: dict[str, _Entry] = {}

    def put(self, key: str, value: Any, cache_control: str, now: float) -> bool:
        policy = parse_cache_control(cache_control)
        ttl = policy.max_age if policy.max_age is not None else 0
        self._entries[key] = _Entry(
            value=value,
            expires_at=now + ttl,
            stale_until=now + ttl + policy.stale_if_error,
        )
        return True

    def get(self, key: str, now: float, on_error: bool = False) -> Any | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        if now <= entry.expires_at:
            return entry.value
        if on_error and now <= entry.stale_until:
            return entry.value
        self._entries.pop(key, None)
        return None
