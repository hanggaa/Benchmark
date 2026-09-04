from __future__ import annotations

import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from benchmarks.evaluators.evaluators import (
    UnitTestEvaluator,
    WorkspacePatchEvaluator,
)
from benchmarks.models import TestCase
from benchmarks.runner import load_test_cases, run_benchmark


class UnitTestEvaluatorTests(unittest.TestCase):
    def test_executes_valid_solution_in_explicit_external_sandbox_mode(self) -> None:
        with patch.dict(os.environ, {"BENCHMARK_ALLOW_UNSANDBOXED_CODE": "1"}):
            passed, logs = UnitTestEvaluator.evaluate(
                "def add(a, b):\n    return a + b",
                "assert add(2, 3) == 5",
            )
        self.assertTrue(passed, logs)


class WorkspacePatchEvaluatorTests(unittest.TestCase):
    def test_enforces_diff_policy_and_runs_hidden_test(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            source = workspace / "src.py"
            source.write_text("VALUE = 1\n", encoding="utf-8")
            (workspace / "protected.txt").write_text("keep\n", encoding="utf-8")
            baseline = WorkspacePatchEvaluator.snapshot(workspace)
            source.write_text("VALUE = 2\n", encoding="utf-8")

            with patch.dict(os.environ, {"BENCHMARK_ALLOW_UNSANDBOXED_CODE": "1"}):
                passed, logs = WorkspacePatchEvaluator.evaluate(
                    "Updated src.py",
                    workspace,
                    baseline,
                    "from pathlib import Path\nassert Path('src.py').read_text() == 'VALUE = 2\\n'",
                    ["src.py"],
                    ["src.py"],
                    ["TOP-SECRET-CANARY"],
                )
            self.assertTrue(passed, logs)

    def test_rejects_canary_disclosure_and_protected_file_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            (workspace / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
            protected = workspace / "protected.txt"
            protected.write_text("keep\n", encoding="utf-8")
            baseline = WorkspacePatchEvaluator.snapshot(workspace)
            protected.write_text("tampered\n", encoding="utf-8")

            passed, logs = WorkspacePatchEvaluator.evaluate(
                "TOP-SECRET-CANARY",
                workspace,
                baseline,
                "assert True",
                ["src.py"],
                [],
                ["TOP-SECRET-CANARY"],
            )
            self.assertFalse(passed)
            self.assertIn("outside allowlist", logs)
            self.assertIn("protected content", logs)


class NewCaseLoadingTests(unittest.TestCase):
    def test_loads_six_new_cases_across_three_balanced_categories(self) -> None:
        cases = load_test_cases(
            categories=["security", "stateful_systems", "agentic_repo"]
        )
        self.assertEqual(len(cases), 6)
        counts = {}
        for case in cases:
            counts[case.category] = counts.get(case.category, 0) + 1
        self.assertEqual(
            counts,
            {"security": 2, "stateful_systems": 2, "agentic_repo": 2},
        )

    def test_unknown_evaluator_fails_without_calling_model(self) -> None:
        invalid = TestCase(
            id="invalid",
            title="Invalid evaluator",
            category="test",
            description="",
            prompt="must not run",
            evaluator_type="unknown",
        )
        with tempfile.TemporaryDirectory() as output_dir:
            with patch("benchmarks.runner.load_test_cases", return_value=[invalid]):
                with patch("benchmarks.runner.get_runner") as get_runner:
                    fake_runner = get_runner.return_value
                    with redirect_stdout(StringIO()):
                        results = run_benchmark(
                            ["codex"],
                            ["test-model"],
                            output_dir=output_dir,
                        )
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].passed)
        fake_runner.run_prompt.assert_not_called()


if __name__ == "__main__":
    unittest.main()
