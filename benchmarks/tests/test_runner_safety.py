from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from benchmarks.runners.antigravity_runner import AntigravityRunner
from benchmarks.runners.claude_runner import ClaudeRunner
from benchmarks.runners.codex_runner import CodexRunner
from benchmarks.runners.opencode_runner import OpenCodeRunner


class AgenticRunnerSafetyTests(unittest.TestCase):
    def _completed(self, stdout: str = "{}") -> SimpleNamespace:
        return SimpleNamespace(returncode=0, stdout=stdout, stderr="")

    def test_codex_uses_workspace_sandbox_for_fixture(self) -> None:
        with patch(
            "benchmarks.runners.codex_runner.subprocess.run",
            return_value=self._completed(),
        ) as run:
            CodexRunner({}).run_prompt("fix", "gpt-test", cwd="/tmp/fixture")
        command = run.call_args.args[0]
        self.assertIn("workspace-write", command)
        self.assertIn("--skip-git-repo-check", command)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)

    def test_claude_uses_safe_mode_for_fixture(self) -> None:
        with patch(
            "benchmarks.runners.claude_runner.subprocess.run",
            return_value=self._completed(),
        ) as run:
            ClaudeRunner({}).run_prompt("fix", "claude-test", cwd="/tmp/fixture")
        command = run.call_args.args[0]
        self.assertIn("--safe-mode", command)
        self.assertIn("dontAsk", command)
        self.assertNotIn("--dangerously-skip-permissions", command)

    def test_antigravity_uses_native_sandbox_for_fixture(self) -> None:
        with patch(
            "benchmarks.runners.antigravity_runner.subprocess.run",
            return_value=self._completed(),
        ) as run:
            AntigravityRunner({}).run_prompt("fix", "gemini-test", cwd="/tmp/fixture")
        command = run.call_args.args[0]
        self.assertIn("--sandbox", command)
        self.assertNotIn("--dangerously-skip-permissions", command)

    def test_opencode_disables_external_plugins_for_fixture(self) -> None:
        with patch(
            "benchmarks.runners.opencode_runner.subprocess.run",
            return_value=self._completed(),
        ) as run:
            OpenCodeRunner({}).run_prompt("fix", "provider/model", cwd="/tmp/fixture")
        self.assertIn("--pure", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
