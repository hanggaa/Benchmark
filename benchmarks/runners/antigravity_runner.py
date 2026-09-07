from __future__ import annotations

import json
import logging
import os
import subprocess
import time
from typing import Any, Dict, Optional, Tuple

from benchmarks.models import TokenUsage
from benchmarks.runners.base_runner import BaseRunner

logger = logging.getLogger(__name__)


class AntigravityRunner(BaseRunner):
    """Runner for Antigravity CLI (agy)."""

    @staticmethod
    def _permission_denial(stderr: str) -> Optional[str]:
        """Surface AGY headless soft-denials, which may still exit successfully."""
        lowered = stderr.lower()
        markers = (
            "permission check failed",
            "denied permission",
            "permission was denied",
            "tool call was denied",
        )
        if not stderr or not any(marker in lowered for marker in markers):
            return None

        detail = next(
            (line.strip() for line in stderr.splitlines() if line.strip()),
            "tool execution was denied",
        )
        return (
            "AGY tool permission was denied in headless mode. Configure "
            "toolPermission='proceed-in-sandbox' and keep terminal sandboxing "
            f"enabled, then retry. CLI detail: {detail}"
        )

    def run_prompt(
        self,
        prompt: str,
        model: str,
        effort: Optional[str] = None,
        timeout_seconds: int = 300,
        cwd: Optional[str] = None,
        workspace_mode: bool = False,
    ) -> Tuple[str, TokenUsage, float, Optional[str]]:
        cmd = [
            "agy",
            "-p",
            prompt,
            "--output-format",
            "json",
            "--print-timeout",
            f"{timeout_seconds}s",
        ]

        cmd.extend([
            "--sandbox",
            "--mode",
            "accept-edits" if workspace_mode else "plan",
            "--disable-slash-commands",
        ])

        # Antigravity does not infer an active workspace from the subprocess
        # working directory alone. Without an explicit project it falls back
        # to the user's global scratch directory, so repository-edit cases
        # cannot see the isolated fixture passed through ``cwd``.
        if cwd:
            cmd.append("--new-project")

        if model:
            cmd.extend(["--model", model])
        if effort and not any(f"({e})" in model.lower() for e in ("high", "medium", "low")):
            cmd.extend(["--effort", effort])

        start_time = time.perf_counter()
        token_usage = TokenUsage()
        pricing = self.get_pricing(model)

        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                cwd=cwd or os.getcwd(),
            )
            duration = time.perf_counter() - start_time

            stdout = process.stdout.strip()
            stderr = process.stderr.strip()

            if process.returncode != 0:
                err_msg = stderr or stdout or f"Process exited with code {process.returncode}"
                return "", token_usage, duration, err_msg

            try:
                data = json.loads(stdout)
                response_text = data.get("response", "")
                usage_data = data.get("usage", {})

                token_usage.input_tokens = usage_data.get("input_tokens", 0)
                token_usage.thinking_tokens = usage_data.get("thinking_tokens", 0)
                raw_output = usage_data.get("output_tokens", 0)
                token_usage.output_tokens = max(
                    raw_output - token_usage.thinking_tokens, 0
                )
                token_usage.cache_read_tokens = usage_data.get("cache_read_tokens", 0)
                token_usage.total_tokens = (
                    token_usage.input_tokens
                    + token_usage.cache_read_tokens
                    + token_usage.output_tokens
                    + token_usage.thinking_tokens
                )
                token_usage.telemetry_source = "agy-json"
                token_usage.telemetry_complete = all(
                    key in usage_data for key in ("input_tokens", "output_tokens")
                )
                token_usage.calculate_cost(pricing)

                permission_error = self._permission_denial(stderr)
                if permission_error:
                    return "", token_usage, duration, permission_error

                if not isinstance(response_text, str):
                    return (
                        "",
                        token_usage,
                        duration,
                        "AGY JSON response field was not text.",
                    )
                if not workspace_mode and not response_text.strip():
                    return (
                        "",
                        token_usage,
                        duration,
                        "AGY completed without a final text response.",
                    )

                return response_text, token_usage, duration, None
            except json.JSONDecodeError:
                # If stdout is plain text
                token_usage.calculate_cost(pricing)
                permission_error = self._permission_denial(stderr)
                if permission_error:
                    return "", token_usage, duration, permission_error
                return stdout, token_usage, duration, None

        except subprocess.TimeoutExpired:
            duration = time.perf_counter() - start_time
            token_usage.input_tokens = self.estimate_prompt_tokens(prompt)
            token_usage.total_tokens = token_usage.input_tokens
            token_usage.telemetry_source = "prompt-estimate"
            token_usage.calculate_cost(pricing)
            return "", token_usage, duration, f"TIMEOUT: Process exceeded {timeout_seconds}s limit"
        except Exception as e:
            duration = time.perf_counter() - start_time
            return "", token_usage, duration, str(e)
