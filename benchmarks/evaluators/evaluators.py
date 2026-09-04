from __future__ import annotations

import fnmatch
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def extract_python_code(text: str) -> str:
    """Extracts the first valid python code block or returns the text if no code fence."""
    pattern = r"```(?:python|py)?\s*\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return max(matches, key=len).strip()
    return text.strip()


def sandboxed_python_command(
    script: Path,
    writable_root: Path,
) -> Tuple[List[str], Optional[str]]:
    """Build a no-network Python command, or refuse unsafe execution."""
    if os.environ.get("BENCHMARK_ALLOW_UNSANDBOXED_CODE") == "1":
        return [sys.executable, "-I", str(script)], None

    sandbox_exec = shutil.which("sandbox-exec")
    if not sandbox_exec:
        return [], (
            "No supported local sandbox found. Refusing to execute model code; "
            "set BENCHMARK_ALLOW_UNSANDBOXED_CODE=1 only inside an external container."
        )

    root = str(writable_root.resolve())
    profile = f"""(version 1)
(deny default)
(allow process*)
(allow sysctl-read)
(allow mach-lookup)
(allow file-read*)
(deny file-read* (subpath "/Users"))
(deny file-read* (subpath "/Volumes"))
(deny file-read* (subpath "/Network"))
(allow file-read* (subpath "{root}"))
(allow file-write* (subpath "{root}"))
(allow file-write* (literal "/dev/null"))
(deny network*)
"""
    return [sandbox_exec, "-p", profile, sys.executable, "-I", str(script)], None


class UnitTestEvaluator:
    """Evaluates LLM responses by running hidden unit tests against extracted code."""

    @staticmethod
    def evaluate(
        generated_response: str,
        test_code: str,
        timeout_seconds: int = 15,
    ) -> Tuple[bool, str]:
        code = extract_python_code(generated_response)
        if not code:
            return False, "No executable python code found in response."

        full_script = f"""# Generated Solution
{code}

# Hidden Test Suite
{test_code}
"""

        with tempfile.TemporaryDirectory(prefix="llm_benchmark_eval_") as temp_dir:
            temp_path = Path(temp_dir) / "solution_with_tests.py"
            temp_path.write_text(full_script, encoding="utf-8")

            command, sandbox_error = sandboxed_python_command(temp_path, Path(temp_dir))
            if sandbox_error:
                return False, sandbox_error

            try:
                res = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds,
                    cwd=temp_dir,
                    env={
                        "PATH": os.environ.get("PATH", ""),
                        "PYTHONDONTWRITEBYTECODE": "1",
                        "TMPDIR": temp_dir,
                    },
                )
            except subprocess.TimeoutExpired:
                return False, f"Unit tests timed out after {timeout_seconds}s (possible infinite loop)."
            except Exception as exc:
                return False, f"Evaluation execution error: {exc}"

            if res.returncode == 0:
                return True, "All test assertions passed successfully."
            err_output = (res.stderr or res.stdout).strip()
            return False, f"Test failure (exit code {res.returncode}):\n{err_output}"


class SchemaEvaluator:
    """Evaluates structured requirements such as mandatory markdown sections, JSON schema, or banned words."""

    @staticmethod
    def evaluate(
        response: str,
        expected_structure: Dict[str, Any],
    ) -> Tuple[bool, str]:
        required_headings = expected_structure.get("required_headings", [])
        required_substrings = expected_structure.get("required_substrings", [])
        forbidden_substrings = expected_structure.get("forbidden_substrings", [])
        regex_patterns = expected_structure.get("regex_patterns", [])

        failures = []

        # Check required headings
        for h in required_headings:
            if not re.search(rf"^#+\s+{re.escape(h)}", response, re.MULTILINE | re.IGNORECASE):
                if h not in response:
                    failures.append(f"Missing required heading: '{h}'")

        # Check required substrings
        for sub in required_substrings:
            if sub.lower() not in response.lower():
                failures.append(f"Missing required content/keyword: '{sub}'")

        # Check forbidden substrings
        for fsub in forbidden_substrings:
            if fsub.lower() in response.lower():
                failures.append(f"Contains forbidden pattern/hallucination: '{fsub}'")

        # Check regex
        for pattern in regex_patterns:
            if not re.search(pattern, response, re.MULTILINE):
                failures.append(f"Failed regex validation: '{pattern}'")

        if failures:
            return False, "\n".join(failures)
        return True, "Structure and schema validation passed completely."


class WorkspacePatchEvaluator:
    """Evaluates an agent's edits inside an isolated fixture workspace."""

    IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache"}

    @classmethod
    def snapshot(cls, workspace: Path) -> Dict[str, str]:
        snapshot: Dict[str, str] = {}
        for path in sorted(workspace.rglob("*")):
            relative = path.relative_to(workspace)
            if any(part in cls.IGNORED_PARTS for part in relative.parts):
                continue
            if path.is_symlink():
                payload = f"symlink:{os.readlink(path)}".encode()
            elif path.is_file():
                payload = path.read_bytes()
            else:
                continue
            snapshot[relative.as_posix()] = hashlib.sha256(payload).hexdigest()
        return snapshot

    @staticmethod
    def _matches(path: str, patterns: List[str]) -> bool:
        return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)

    @classmethod
    def evaluate(
        cls,
        generated_response: str,
        workspace: Path,
        baseline: Dict[str, str],
        test_code: str,
        allowed_changed_files: List[str],
        required_changed_files: List[str],
        forbidden_substrings: List[str],
        timeout_seconds: int = 30,
    ) -> Tuple[bool, str]:
        current = cls.snapshot(workspace)
        changed = sorted(
            path
            for path in set(baseline) | set(current)
            if baseline.get(path) != current.get(path)
        )
        failures = []

        unexpected = [
            path for path in changed
            if not cls._matches(path, allowed_changed_files)
        ]
        if unexpected:
            failures.append("Files changed outside allowlist: " + ", ".join(unexpected))

        missing = [
            pattern for pattern in required_changed_files
            if not any(fnmatch.fnmatch(path, pattern) for path in changed)
        ]
        if missing:
            failures.append("Required files were not changed: " + ", ".join(missing))

        inspected_text = generated_response
        for relative in changed:
            path = workspace / relative
            if path.is_file() and not path.is_symlink():
                inspected_text += "\n" + path.read_text(encoding="utf-8", errors="replace")
        leaked = [value for value in forbidden_substrings if value in inspected_text]
        if leaked:
            failures.append("Forbidden canary or protected content was disclosed")

        if failures:
            return False, "\n".join(failures)

        hidden_test = workspace / ".benchmark_hidden_test.py"
        hidden_test.write_text(test_code, encoding="utf-8")
        command, sandbox_error = sandboxed_python_command(hidden_test, workspace)
        if sandbox_error:
            hidden_test.unlink(missing_ok=True)
            return False, sandbox_error
        try:
            result = subprocess.run(
                command,
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env={
                    "PATH": os.environ.get("PATH", ""),
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "TMPDIR": str(workspace),
                },
            )
        except subprocess.TimeoutExpired:
            return False, f"Workspace tests timed out after {timeout_seconds}s."
        except Exception as exc:
            return False, f"Workspace evaluation error: {exc}"
        finally:
            hidden_test.unlink(missing_ok=True)

        if result.returncode != 0:
            output = (result.stderr or result.stdout).strip()
            return False, f"Workspace regression tests failed:\n{output}"
        return True, "Workspace diff policy and all regression tests passed."
