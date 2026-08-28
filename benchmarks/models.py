from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import time

@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    thinking_tokens: int = 0
    cache_read_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0

    def calculate_cost(self, pricing: Dict[str, float]) -> float:
        cost = (
            (self.input_tokens / 1_000_000) * pricing.get('input', 0.0)
            + (self.output_tokens / 1_000_000) * pricing.get('output', 0.0)
            + (self.thinking_tokens / 1_000_000) * pricing.get('thinking', pricing.get('output', 0.0))
            + (self.cache_read_tokens / 1_000_000) * pricing.get('cache_read', 0.0)
        )
        self.estimated_cost_usd = round(cost, 6)
        return self.estimated_cost_usd


@dataclass
class TestCase:
    id: str
    title: str
    category: str  # 'logic', 'bugfix', 'research', 'tool_use'
    description: str
    prompt: str
    evaluator_type: str  # 'python_unit_test', 'schema_check', 'string_contains'
    test_code: str = ''
    expected_structure: Dict[str, Any] = field(default_factory=dict)
    timeout_seconds: int = 300
    difficulty: str = 'medium'  # 'easy', 'medium', 'hard'


@dataclass
class BenchmarkResult:
    case_id: str
    case_title: str
    category: str
    model: str
    cli: str
    passed: bool
    duration_seconds: float
    token_usage: TokenUsage
    raw_response: str = ''
    error_message: Optional[str] = None
    evaluator_logs: str = ''
    effort: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ModelSummary:
    model: str
    cli: str
    effort: Optional[str]
    total_cases: int
    passed_cases: int
    pass_rate: float
    avg_duration_seconds: float
    total_input_tokens: int
    total_output_tokens: int
    total_thinking_tokens: int
    total_cost_usd: float
    efficiency_score: float  # (pass_rate * 100) / (cost + 0.01)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
