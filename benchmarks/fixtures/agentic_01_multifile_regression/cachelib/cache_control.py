from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CachePolicy:
    max_age: int | None = None
    no_store: bool = False
    stale_if_error: int = 0


def parse_cache_control(header: str) -> CachePolicy:
    """Parse the small Cache-Control subset used by HTTPCache."""
    values: dict[str, str | bool] = {}
    for raw_directive in header.split(","):
        directive = raw_directive.strip()
        if "=" in directive:
            name, value = directive.split("=", 1)
            values[name.strip()] = value.strip().strip('"')
        elif directive:
            values[directive] = True

    max_age = int(values["max-age"]) if "max-age" in values else None
    stale = int(values.get("stale-if-error", 0))
    return CachePolicy(
        max_age=max_age,
        no_store="no-store" in values,
        stale_if_error=stale,
    )
