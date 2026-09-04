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

    def run_prompt(
        self,
        prompt: str,
        model: str,
        effort: Optional[str] = None,
        timeout_seconds: int = 300,
        cwd: Optional[str] = None,
    ) -> Tuple[str, TokenUsage, float, Optional[str]]:
        cmd = [
            "agy",
            "-p",
            prompt,
            "--output-format",
            "json",
        ]

        if cwd:
            cmd.extend(["--sandbox", "--mode", "accept-edits", "--disable-slash-commands"])
        else:
            cmd.append("--dangerously-skip-permissions")

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
                response_text = data.get("response", stdout)
                reported_duration = data.get("duration_seconds", duration)
                usage_data = data.get("usage", {})

                token_usage.input_tokens = usage_data.get("input_tokens", 0)
                token_usage.output_tokens = usage_data.get("output_tokens", 0)
                token_usage.thinking_tokens = usage_data.get("thinking_tokens", 0)
                token_usage.cache_read_tokens = usage_data.get("cache_read_tokens", 0)
                token_usage.total_tokens = usage_data.get("total_tokens", 0)
                token_usage.calculate_cost(pricing)

                return response_text, token_usage, reported_duration, None
            except json.JSONDecodeError:
                # If stdout is plain text
                token_usage.calculate_cost(pricing)
                return stdout, token_usage, duration, None

        except subprocess.TimeoutExpired:
            duration = time.perf_counter() - start_time
            token_usage.input_tokens = self.estimate_prompt_tokens(prompt)
            token_usage.total_tokens = token_usage.input_tokens
            token_usage.calculate_cost(pricing)
            return "", token_usage, duration, f"TIMEOUT: Process exceeded {timeout_seconds}s limit"
        except Exception as e:
            duration = time.perf_counter() - start_time
            return "", token_usage, duration, str(e)
