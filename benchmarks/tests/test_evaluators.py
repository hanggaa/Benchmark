from __future__ import annotations

import base64
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from benchmarks.evaluators.evaluators import (
    SchemaEvaluator,
    UnitTestEvaluator,
    WorkspacePatchEvaluator,
    extract_python_code,
)
from benchmarks.models import TestCase, TokenUsage
from benchmarks.runner import (
    BenchmarkConfigurationError,
    hash_workspace_fixture,
    load_test_cases,
    parse_model_spec,
    run_benchmark,
)


class UnitTestEvaluatorTests(unittest.TestCase):
    def test_extracts_first_syntactically_valid_python_block(self) -> None:
        response = """```python
def broken(:
```
explanation
```python
def valid():
    return True
```
"""
        self.assertIn("def valid", extract_python_code(response))

    def test_executes_valid_solution_in_explicit_external_sandbox_mode(self) -> None:
        with patch.dict(os.environ, {"BENCHMARK_ALLOW_UNSANDBOXED_CODE": "1"}):
            passed, logs = UnitTestEvaluator.evaluate(
                "def add(a, b):\n    return a + b",
                "assert add(2, 3) == 5",
            )
        self.assertTrue(passed, logs)

    def test_rejects_clean_early_exit_without_running_tests(self) -> None:
        for response in ("raise SystemExit(0)", "import os\nos._exit(0)"):
            with self.subTest(response=response):
                with patch.dict(
                    os.environ, {"BENCHMARK_ALLOW_UNSANDBOXED_CODE": "1"}
                ):
                    passed, logs = UnitTestEvaluator.evaluate(
                        response,
                        "raise AssertionError('test suite must execute')",
                    )
                self.assertFalse(passed)


class SchemaEvaluatorTests(unittest.TestCase):
    def test_rejects_keyword_stuffing_without_real_heading_or_length(self) -> None:
        passed, logs = SchemaEvaluator.evaluate(
            "Nonsense Recommendation Matrix pgvector Qdrant Pinecone | Engine | $",
            {
                "required_headings": ["Recommendation Matrix"],
                "required_substrings": ["pgvector", "Qdrant", "Pinecone"],
                "min_words": 100,
            },
        )
        self.assertFalse(passed)
        self.assertIn("Missing required heading", logs)
        self.assertIn("minimum is 100", logs)

    def test_section_word_count_includes_nested_subheadings(self) -> None:
        response = """## Target Persona & Key Pain Points

### Target Personas
Backend developers need actionable explanations for slow database queries.

### Key Pain Points
Execution plans are difficult to interpret without specialist database knowledge.

## Next Section
Unrelated content must not count toward the previous section.
"""
        passed, logs = SchemaEvaluator.evaluate(
            response,
            {
                "min_section_words": {
                    "Target Persona & Key Pain Points": 18,
                }
            },
        )
        self.assertTrue(passed, logs)

    def test_table_row_accepts_markdown_and_parenthetical_qualifier(self) -> None:
        response = """| Engine | Cost |
| --- | --- |
| **pgvector** (PostgreSQL) | $100 |
"""
        passed, logs = SchemaEvaluator.evaluate(
            response,
            {
                "required_table_columns": ["Engine", "Cost"],
                "required_table_first_column_values": ["pgvector"],
            },
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

    def test_rejects_encoded_canary_disclosure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            baseline = WorkspacePatchEvaluator.snapshot(workspace)
            encoded = base64.b64encode(b"TOP-SECRET-CANARY").decode("ascii")
            passed, logs = WorkspacePatchEvaluator.evaluate(
                encoded,
                workspace,
                baseline,
                "assert True",
                [],
                [],
                ["TOP-SECRET-CANARY"],
            )
            self.assertFalse(passed)
            self.assertIn("protected content", logs)

    def test_rejects_git_metadata_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            source = workspace / "src.py"
            source.write_text("VALUE = 1\n", encoding="utf-8")
            baseline = WorkspacePatchEvaluator.snapshot(workspace)
            hook = workspace / ".git" / "hooks" / "post-checkout"
            hook.parent.mkdir(parents=True)
            hook.write_text("malicious\n", encoding="utf-8")

            passed, logs = WorkspacePatchEvaluator.evaluate(
                "done",
                workspace,
                baseline,
                "assert True",
                ["src.py"],
                [],
                [],
            )
            self.assertFalse(passed)
            self.assertIn(".git/hooks/post-checkout", logs)

    def test_workspace_early_exit_cannot_forge_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            source = workspace / "solution.py"
            source.write_text("VALUE = 1\n", encoding="utf-8")
            baseline = WorkspacePatchEvaluator.snapshot(workspace)
            source.write_text("import os\nos._exit(0)\n", encoding="utf-8")
            held_out_test = """import importlib.util
from pathlib import Path
assert not Path(__file__).exists(), 'held-out test leaked into workspace'
spec = importlib.util.spec_from_file_location('solution', Path(__file__).with_name('solution.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
raise AssertionError('must execute')
"""
            with patch.dict(
                os.environ, {"BENCHMARK_ALLOW_UNSANDBOXED_CODE": "1"}
            ):
                passed, logs = WorkspacePatchEvaluator.evaluate(
                    "done",
                    workspace,
                    baseline,
                    held_out_test,
                    ["solution.py"],
                    ["solution.py"],
                    [],
                )
            self.assertFalse(passed)
            self.assertIn("completion proof", logs)

    def test_rejects_oversized_workspace_artifact_before_reading_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            baseline = WorkspacePatchEvaluator.snapshot(workspace)
            oversized = workspace / "oversized.bin"
            with oversized.open("wb") as handle:
                handle.truncate(WorkspacePatchEvaluator.MAX_SNAPSHOT_FILE_BYTES + 1)
            passed, logs = WorkspacePatchEvaluator.evaluate(
                "done",
                workspace,
                baseline,
                "assert True",
                ["oversized.bin"],
                [],
                [],
            )
            self.assertFalse(passed)
            self.assertIn("Workspace snapshot rejected", logs)


class NewCaseLoadingTests(unittest.TestCase):
    def test_workspace_fixture_hash_tracks_sources_not_runtime_cache(self) -> None:
        with tempfile.TemporaryDirectory() as fixture_dir:
            fixture = Path(fixture_dir)
            source = fixture / "module.py"
            source.write_text("VALUE = 1\n", encoding="utf-8")
            initial = hash_workspace_fixture(fixture)

            cache = fixture / "__pycache__"
            cache.mkdir()
            (cache / "module.cpython-313.pyc").write_bytes(b"runtime-cache")
            self.assertEqual(hash_workspace_fixture(fixture), initial)

            source.write_text("VALUE = 2\n", encoding="utf-8")
            self.assertNotEqual(hash_workspace_fixture(fixture), initial)

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

    def test_ctf_cases_are_reported_as_their_own_category(self) -> None:
        cases = load_test_cases(categories=["ctf"])
        self.assertEqual(
            [case.id for case in cases],
            ["sec_ctf_01_keygen", "sec_ctf_02_sql_ast_firewall"],
        )

    def test_agentic_injection_contract_covers_held_out_input_classes(self) -> None:
        contract = (
            Path(__file__).parents[1]
            / "fixtures"
            / "agentic_02_indirect_injection"
            / "docs"
            / "vendor_payload.md"
        ).read_text(encoding="utf-8")
        normalized_contract = " ".join(contract.split())
        for requirement in (
            "heterogeneous JSON array",
            "non-object elements must be skipped",
            "exactly three ASCII letters",
            "at most two fractional digits",
            "later invalid duplicate does not erase",
            "must not mutate",
        ):
            self.assertIn(requirement, normalized_contract)

    def test_private_test_override_is_preferred(self) -> None:
        with tempfile.TemporaryDirectory() as private_dir:
            private_test = Path(private_dir) / "logic_02_topo_cycle.py"
            private_test.write_text("assert PRIVATE_SENTINEL\n", encoding="utf-8")
            cases = load_test_cases(
                case_ids=["logic_02_topo_cycle"],
                private_tests_dir=private_dir,
            )
        self.assertEqual(len(cases), 1)
        self.assertEqual(cases[0].test_code, "assert PRIVATE_SENTINEL\n")
        self.assertEqual(cases[0].test_source, "private")

    def test_parses_cli_model_effort_suffix(self) -> None:
        self.assertEqual(
            parse_model_spec("codex:gpt-5.6-sol:high"),
            ("codex", "gpt-5.6-sol", "high"),
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
        web_data = Path(__file__).parents[2] / "src" / "data" / "benchmark-data.json"
        before = web_data.read_bytes()
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
        self.assertEqual(web_data.read_bytes(), before)

    def test_dry_run_creates_no_report_files(self) -> None:
        with tempfile.TemporaryDirectory() as output_dir:
            with redirect_stdout(StringIO()):
                results = run_benchmark(
                    ["codex"],
                    ["gpt-test"],
                    case_ids=["logic_02_topo_cycle"],
                    output_dir=output_dir,
                    dry_run=True,
                )
            self.assertEqual(results, [])
            self.assertEqual(list(Path(output_dir).iterdir()), [])

    def test_response_only_case_uses_ephemeral_workspace(self) -> None:
        case = TestCase(
            id="isolated",
            title="Isolated response",
            category="test",
            description="",
            prompt="solve",
            evaluator_type="python_unit_test",
            test_code="assert True",
            case_hash="abc",
        )
        with tempfile.TemporaryDirectory() as output_dir:
            with patch("benchmarks.runner.load_test_cases", return_value=[case]):
                with patch("benchmarks.runner.get_runner") as get_runner:
                    get_runner.return_value.run_prompt.return_value = (
                        "def answer():\n    return 1",
                        TokenUsage(),
                        0.1,
                        None,
                    )
                    with patch(
                        "benchmarks.runner.UnitTestEvaluator.evaluate",
                        return_value=(True, "ok"),
                    ):
                        with redirect_stdout(StringIO()):
                            run_benchmark(
                                ["codex"],
                                ["gpt-test"],
                                output_dir=output_dir,
                            )
        kwargs = get_runner.return_value.run_prompt.call_args.kwargs
        self.assertFalse(kwargs["workspace_mode"])
        self.assertNotEqual(Path(kwargs["cwd"]), Path.cwd())
        self.assertFalse(Path(kwargs["cwd"]).exists())

    def test_publish_rejects_filtered_runs_before_model_calls(self) -> None:
        with self.assertRaises(BenchmarkConfigurationError):
            run_benchmark(
                ["codex"],
                ["gpt-test"],
                case_ids=["logic_02_topo_cycle"],
                publish=True,
            )

    def test_publish_rejects_cli_errors(self) -> None:
        case = TestCase(
            id="case",
            title="Case",
            category="logic",
            description="",
            prompt="solve",
            evaluator_type="python_unit_test",
            test_code="assert True",
            case_hash="abc",
        )
        with tempfile.TemporaryDirectory() as output_dir:
            with patch("benchmarks.runner.load_test_cases", return_value=[case]):
                with patch("benchmarks.runner.get_runner") as get_runner:
                    get_runner.return_value.run_prompt.return_value = (
                        "",
                        TokenUsage(),
                        0.1,
                        "CLI permission denied",
                    )
                    with redirect_stdout(StringIO()):
                        with self.assertRaisesRegex(
                            BenchmarkConfigurationError,
                            "CLI/infrastructure error",
                        ):
                            run_benchmark(
                                ["codex"],
                                ["gpt-test"],
                                output_dir=output_dir,
                                publish=True,
                            )


if __name__ == "__main__":
    unittest.main()
