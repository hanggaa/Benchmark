from __future__ import annotations

from decimal import Decimal
from typing import Any


def normalize_orders(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Normalize vendor order records for deterministic downstream processing."""
    normalized = []
    for record in records:
        normalized.append(
            {
                "order_id": str(record["order_id"]),
                "currency": str(record["currency"]),
                "amount": str(Decimal(str(record["amount"]))),
            }
        )
    return normalized
