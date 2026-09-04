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


class CodexRunner(BaseRunner):
    """Runner for Codex CLI (codex) with JSONL event stream parsing."""

    def run_prompt(
        self,
        prompt: str,
        model: str,
        effort: Optional[str] = None,
        timeout_seconds: int = 300,
        cwd: Optional[str] = None,
    ) -> Tuple[str, TokenUsage, float, Optional[str]]:
        clean_model = model
        model_effort = effort

        if " --effort " in clean_model:
            parts = clean_model.split(" --effort ")
            clean_model = parts[0].strip()
            model_effort = parts[1].strip()
        elif ":" in clean_model and not clean_model.startswith("http"):
            parts = clean_model.split(":")
            if parts[1].lower() in ("low", "medium", "high"):
                clean_model = parts[0].strip()
                model_effort = parts[1].strip()

        cmd = [
            "codex",
            "exec",
            "--ephemeral",
            "--json",
        ]

        if cwd:
            cmd.extend([
                "--sandbox",
                "workspace-write",
                "--ignore-user-config",
                "--ignore-rules",
                "--skip-git-repo-check",
                "--cd",
                cwd,
            ])
        else:
            cmd.append("--dangerously-bypass-approvals-and-sandbox")

        if clean_model:
            cmd.extend(["-m", clean_model])

        if model_effort:
            cmd.extend(["-c", f'model_reasoning_effort="{model_effort}"'])

        cmd.append(prompt)

        start_time = time.perf_counter()
        token_usage = TokenUsage()
        pricing = self.get_pricing(clean_model)
        collected_responses = []

        try:
            process = subprocess.run(
                cmd,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                cwd=cwd or os.getcwd(),
            )
            duration = time.perf_counter() - start_time
            stdout = process.stdout.strip()
            stderr = process.stderr.strip()

            # Parse JSONL events from stdout
            for line in stdout.splitlines():
                line = line.strip()
                if not line or not line.startswith("{"):
                    continue
                try:
                    event = json.loads(line)
                    event_type = event.get("type", "")

                    # Collect agent message content
                    if event_type == "item.completed":
                        item = event.get("item", {})
                        if item.get("type") == "agent_message":
                            text_content = item.get("text", "")
                            if text_content:
                                collected_responses.append(text_content)

                    # Collect usage tokens
                    elif event_type == "turn.completed":
                        usage = event.get("usage", {})
                        token_usage.input_tokens = usage.get("input_tokens", 0)
                        token_usage.cache_read_tokens = usage.get("cached_input_tokens", 0)
                        token_usage.output_tokens = usage.get("output_tokens", 0)
                        token_usage.thinking_tokens = usage.get("reasoning_output_tokens", 0)
                        token_usage.total_tokens = (
                            token_usage.input_tokens + token_usage.output_tokens
                        )
                except json.JSONDecodeError:
                    continue

            response_text = "\n\n".join(collected_responses).strip() if collected_responses else stdout

            if process.returncode != 0 and not response_text:
                err_msg = stderr or stdout or f"Process exited with code {process.returncode}"
                return "", token_usage, duration, err_msg

            token_usage.calculate_cost(pricing)
            return response_text, token_usage, duration, None

        except subprocess.TimeoutExpired:
            duration = time.perf_counter() - start_time
            token_usage.input_tokens = self.estimate_prompt_tokens(prompt)
            token_usage.total_tokens = token_usage.input_tokens
            token_usage.calculate_cost(pricing)
            return "", token_usage, duration, f"TIMEOUT: Process exceeded {timeout_seconds}s limit"
        except Exception as e:
            duration = time.perf_counter() - start_time
            return "", token_usage, duration, str(e)
