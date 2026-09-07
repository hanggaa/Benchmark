from __future__ import annotations

import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from benchmarks.runners.antigravity_runner import AntigravityRunner
from benchmarks.runners.claude_runner import ClaudeRunner
from benchmarks.runners.codex_runner import CodexRunner
from benchmarks.runners.opencode_runner import OpenCodeRunner


class AgenticRunnerSafetyTests(unittest.TestCase):
    def _completed(self, stdout: str = "{}", stderr: str = "") -> SimpleNamespace:
        return SimpleNamespace(returncode=0, stdout=stdout, stderr=stderr)

    def test_codex_uses_workspace_sandbox_for_fixture(self) -> None:
        with patch(
            "benchmarks.runners.codex_runner.subprocess.run",
            return_value=self._completed(),
        ) as run:
            CodexRunner({}).run_prompt(
                "fix", "gpt-test", cwd="/tmp/fixture", workspace_mode=True
            )
        command = run.call_args.args[0]
        self.assertIn("workspace-write", command)
        self.assertIn("--skip-git-repo-check", command)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)

    def test_claude_uses_safe_mode_for_fixture(self) -> None:
        with patch(
            "benchmarks.runners.claude_runner.subprocess.run",
            return_value=self._completed(),
        ) as run:
            ClaudeRunner({}).run_prompt(
                "fix", "claude-test", cwd="/tmp/fixture", workspace_mode=True
            )
        command = run.call_args.args[0]
        self.assertIn("--safe-mode", command)
        self.assertIn("dontAsk", command)
        self.assertNotIn("--dangerously-skip-permissions", command)

    def test_antigravity_uses_native_sandbox_for_fixture(self) -> None:
        with patch(
            "benchmarks.runners.antigravity_runner.subprocess.run",
            return_value=self._completed(),
        ) as run:
            AntigravityRunner({}).run_prompt(
                "fix", "gemini-test", cwd="/tmp/fixture", workspace_mode=True
            )
        command = run.call_args.args[0]
        self.assertIn("--sandbox", command)
        self.assertIn("--new-project", command)
        self.assertIn("--print-timeout", command)
        timeout_index = command.index("--print-timeout")
        self.assertEqual(command[timeout_index + 1], "300s")
        self.assertNotIn("--dangerously-skip-permissions", command)

    def test_antigravity_response_case_rejects_empty_final_text(self) -> None:
        stdout = (
            '{"response":"","usage":{"input_tokens":100,'
            '"output_tokens":20,"thinking_tokens":10}}'
        )
        with patch(
            "benchmarks.runners.antigravity_runner.subprocess.run",
            return_value=self._completed(stdout),
        ):
            response, usage, _, error = AntigravityRunner({}).run_prompt(
                "solve", "gemini-test", cwd="/tmp/prompt", workspace_mode=False
            )
        self.assertEqual(response, "")
        self.assertEqual(usage.output_tokens, 10)
        self.assertIn("without a final text response", error)

    def test_antigravity_surfaces_headless_permission_soft_denial(self) -> None:
        stdout = (
            '{"response":"","usage":{"input_tokens":100,'
            '"output_tokens":20,"thinking_tokens":10}}'
        )
        stderr = (
            '[permission check failed for command "pytest": '
            "user denied permission to run command: pytest]"
        )
        with patch(
            "benchmarks.runners.antigravity_runner.subprocess.run",
            return_value=self._completed(stdout, stderr),
        ):
            response, usage, _, error = AntigravityRunner({}).run_prompt(
                "fix", "gemini-test", cwd="/tmp/fixture", workspace_mode=True
            )
        self.assertEqual(response, "")
        self.assertEqual(usage.output_tokens, 10)
        self.assertIn("permission was denied", error)
        self.assertIn("proceed-in-sandbox", error)

    def test_opencode_refuses_agentic_workspace_without_external_sandbox(self) -> None:
        with patch(
            "benchmarks.runners.opencode_runner.subprocess.run",
            return_value=self._completed(),
        ) as run:
            _, _, _, error = OpenCodeRunner({}).run_prompt(
                "fix", "provider/model", cwd="/tmp/fixture", workspace_mode=True
            )
        run.assert_not_called()
        self.assertIn("refused", error)

    def test_opencode_external_sandbox_override_keeps_pure_mode(self) -> None:
        with patch.dict(os.environ, {"BENCHMARK_ALLOW_UNSAFE_OPENCODE": "1"}):
            with patch(
                "benchmarks.runners.opencode_runner.subprocess.run",
                return_value=self._completed(),
            ) as run:
                OpenCodeRunner({}).run_prompt(
                    "fix", "provider/model", cwd="/tmp/fixture", workspace_mode=True
                )
        self.assertIn("--pure", run.call_args.args[0])

    def test_opencode_parses_jsonl_text_and_usage(self) -> None:
        stdout = "\n".join(
            [
                '{"type":"text","part":{"text":"answer"}}',
                '{"type":"step_finish","part":{"tokens":{"input":100,"output":40,"reasoning":10,"cache":{"read":20}}}}',
            ]
        )
        with patch(
            "benchmarks.runners.opencode_runner.subprocess.run",
            return_value=self._completed(stdout),
        ):
            response, usage, _, error = OpenCodeRunner({}).run_prompt(
                "solve", "provider/model", cwd="/tmp/prompt"
            )
        self.assertIsNone(error)
        self.assertEqual(response, "answer")
        self.assertEqual(usage.input_tokens, 100)
        self.assertEqual(usage.output_tokens, 40)
        self.assertEqual(usage.thinking_tokens, 10)
        self.assertEqual(usage.cache_read_tokens, 20)
        self.assertEqual(usage.total_tokens, 170)
        self.assertTrue(usage.telemetry_complete)


if __name__ == "__main__":
    unittest.main()
