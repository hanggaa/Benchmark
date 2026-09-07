from __future__ import annotations

import unittest

from benchmarks.models import BenchmarkResult, TokenUsage
from benchmarks.reporters.reporters import MarkdownReporter


class TokenAccountingTests(unittest.TestCase):
    def test_cached_input_is_not_charged_twice(self) -> None:
        usage = TokenUsage(
            input_tokens=60,
            output_tokens=20,
            cache_read_tokens=40,
            telemetry_complete=True,
        )
        usage.calculate_cost({"input": 10, "output": 20, "cache_read": 1})
        self.assertEqual(usage.estimated_cost_usd, 0.00104)


class ReporterTests(unittest.TestCase):
    def test_efficiency_is_na_when_telemetry_is_incomplete(self) -> None:
        result = BenchmarkResult(
            case_id="case",
            case_title="Case",
            category="logic",
            model="model",
            cli="cli",
            passed=True,
            duration_seconds=1.0,
            token_usage=TokenUsage(),
            difficulty="hard",
        )
        report = MarkdownReporter.generate_report([result])
        self.assertIn("N/A (telemetry incomplete)", report)

    def test_evaluator_timeout_is_included_in_timeout_penalty(self) -> None:
        usage = TokenUsage(
            input_tokens=100,
            output_tokens=100,
            telemetry_source="test",
            telemetry_complete=True,
        )
        result = BenchmarkResult(
            case_id="case",
            case_title="Case",
            category="logic",
            model="model",
            cli="cli",
            passed=False,
            duration_seconds=15.0,
            token_usage=usage,
            evaluator_logs="Tests timed out after 15s.",
            difficulty="hard",
        )
        report = MarkdownReporter.generate_report([result])
        self.assertIn("**0**", report)

    def test_cli_error_is_not_scored_as_model_failure(self) -> None:
        usage = TokenUsage(
            input_tokens=100,
            output_tokens=10,
            telemetry_source="test",
            telemetry_complete=True,
        )
        result = BenchmarkResult(
            case_id="case",
            case_title="Case",
            category="agentic_repo",
            model="model",
            cli="agy",
            passed=False,
            duration_seconds=1.0,
            token_usage=usage,
            error_message="AGY tool permission was denied in headless mode.",
            difficulty="hard",
        )
        report = MarkdownReporter.generate_report([result])
        self.assertIn("**0** scored run(s), **1** CLI error(s)", report)
        self.assertIn("**N/A** (0/0)", report)
        self.assertIn("### ⚠️ CLI ERROR: Case", report)

    def test_detailed_tokens_include_cache_and_total(self) -> None:
        usage = TokenUsage(
            input_tokens=10,
            output_tokens=20,
            thinking_tokens=30,
            cache_read_tokens=40,
            total_tokens=100,
            telemetry_source="test",
            telemetry_complete=True,
        )
        result = BenchmarkResult(
            case_id="case",
            case_title="Case",
            category="logic",
            model="model",
            cli="cli",
            passed=True,
            duration_seconds=1.0,
            token_usage=usage,
        )
        report = MarkdownReporter.generate_report([result])
        self.assertIn("Cache Read: 40", report)
        self.assertIn("Total: 100", report)


if __name__ == "__main__":
    unittest.main()
