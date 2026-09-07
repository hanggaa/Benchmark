from __future__ import annotations

import json
import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from benchmarks.models import TokenUsage
from benchmarks.runners.base_runner import BaseRunner

logger = logging.getLogger(__name__)


class AntigravityRunner(BaseRunner):
    """Runner for Antigravity CLI (agy)."""

    _RESPONSE_ARTIFACT_SUFFIXES = {
        ".c",
        ".cpp",
        ".go",
        ".java",
        ".js",
        ".json",
        ".jsx",
        ".md",
        ".py",
        ".rs",
        ".sh",
        ".ts",
        ".tsx",
        ".txt",
        ".yaml",
        ".yml",
    }

    @staticmethod
    def _workspace_files(cwd: Optional[str]) -> set[str]:
        """Return safe regular files relative to an isolated prompt workspace."""
        if not cwd:
            return set()
        root = Path(cwd)
        if not root.is_dir():
            return set()
        files: set[str] = set()
        for path in root.rglob("*"):
            if path.is_symlink() or not path.is_file():
                continue
            files.add(path.relative_to(root).as_posix())
        return files

    @classmethod
    def _recover_response_artifact(
        cls, cwd: Optional[str], files_before: set[str]
    ) -> Optional[str]:
        """Recover a single text artifact when AGY omits its final response."""
        if not cwd:
            return None
        root = Path(cwd).resolve()
        if not root.is_dir():
            return None

        candidates: list[Path] = []
        for path in root.rglob("*"):
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            hidden = any(
                part.startswith(".") for part in path.relative_to(root).parts
            )
            if relative in files_before or hidden:
                continue
            if path.suffix.lower() not in cls._RESPONSE_ARTIFACT_SUFFIXES:
                continue
            try:
                if path.stat().st_size > 2_000_000:
                    continue
                path.resolve().relative_to(root)
            except (OSError, ValueError):
                continue
            candidates.append(path)

        if len(candidates) != 1:
            return None
        try:
            content = candidates[0].read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return None
        return content if content.strip() else None

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
        files_before = (
            self._workspace_files(cwd) if not workspace_mode else set()
        )
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
            # Response-only cases already run in a disposable empty directory.
            # Allowing edits there prevents AGY's file tool from being denied;
            # the resulting single artifact can then be evaluated as its answer.
            "accept-edits",
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

                agy_error = data.get("error")
                agy_status = str(data.get("status", "")).upper()
                if agy_error or agy_status == "ERROR":
                    return (
                        "",
                        token_usage,
                        duration,
                        str(agy_error or "AGY reported an error status."),
                    )

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
                    artifact = self._recover_response_artifact(cwd, files_before)
                    if artifact is not None:
                        logger.warning(
                            "AGY omitted final text; recovered its single prompt-workspace artifact."
                        )
                        return artifact, token_usage, duration, None
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
