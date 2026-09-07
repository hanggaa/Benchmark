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


class OpenCodeRunner(BaseRunner):
    """Runner for OpenCode CLI (opencode)."""

    @staticmethod
    def _parse_events(stdout: str) -> Tuple[str, Dict[str, int], bool]:
        events = []
        for line in stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)

        texts = []
        normalized: Dict[str, int] = {}
        telemetry_complete = False
        for event in events:
            part = event.get("part") if isinstance(event.get("part"), dict) else {}
            for candidate in (
                part.get("text"),
                event.get("text"),
                event.get("response"),
                event.get("result"),
            ):
                if isinstance(candidate, str) and candidate and candidate not in texts:
                    texts.append(candidate)

            token_data = event.get("usage")
            if not isinstance(token_data, dict):
                token_data = event.get("tokens")
            if not isinstance(token_data, dict):
                token_data = part.get("tokens")
            if not isinstance(token_data, dict):
                continue

            cache = token_data.get("cache", {})
            cache_read = cache.get("read", 0) if isinstance(cache, dict) else 0
            input_tokens = token_data.get(
                "input_tokens", token_data.get("input", 0)
            )
            raw_output = token_data.get(
                "output_tokens", token_data.get("output", 0)
            )
            thinking_tokens = token_data.get(
                "thinking_tokens", token_data.get("reasoning", 0)
            )
            normalized = {
                "input": int(input_tokens or 0),
                "raw_output": int(raw_output or 0),
                "thinking": int(thinking_tokens or 0),
                "cache_read": int(
                    token_data.get(
                        "cache_read_tokens",
                        token_data.get("cache_read", cache_read),
                    )
                    or 0
                ),
            }
            telemetry_complete = any(
                key in token_data for key in ("input_tokens", "input")
            ) and any(key in token_data for key in ("output_tokens", "output"))

        return "\n".join(texts).strip(), normalized, telemetry_complete

    def run_prompt(
        self,
        prompt: str,
        model: str,
        effort: Optional[str] = None,
        timeout_seconds: int = 300,
        cwd: Optional[str] = None,
        workspace_mode: bool = False,
    ) -> Tuple[str, TokenUsage, float, Optional[str]]:
        if workspace_mode and os.environ.get("BENCHMARK_ALLOW_UNSAFE_OPENCODE") != "1":
            return (
                "",
                TokenUsage(),
                0.0,
                "OpenCode agentic workspace execution refused: --pure disables plugins "
                "but is not a filesystem sandbox. Set BENCHMARK_ALLOW_UNSAFE_OPENCODE=1 "
                "only inside an external disposable container.",
            )

        cmd = [
            "opencode",
            "run",
            prompt,
            "--format",
            "json",
        ]

        cmd.append("--pure")

        if model:
            cmd.extend(["-m", model])
        if effort:
            cmd.extend(["--variant", effort])

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

            response_text, usage, complete = self._parse_events(stdout)
            if usage:
                token_usage.input_tokens = usage["input"]
                token_usage.thinking_tokens = usage["thinking"]
                token_usage.output_tokens = usage["raw_output"]
                token_usage.cache_read_tokens = usage["cache_read"]
                token_usage.total_tokens = (
                    token_usage.input_tokens
                    + token_usage.cache_read_tokens
                    + token_usage.output_tokens
                    + token_usage.thinking_tokens
                )
                token_usage.telemetry_source = "opencode-jsonl"
                token_usage.telemetry_complete = complete
            token_usage.calculate_cost(pricing)
            return response_text or stdout, token_usage, duration, None

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
