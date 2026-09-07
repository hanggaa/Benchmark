from __future__ import annotations

import ast
import base64
import fnmatch
import hashlib
import os
import re
import secrets
import signal
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
    for match in matches:
        candidate = match.strip()
        try:
            ast.parse(candidate)
        except SyntaxError:
            continue
        return candidate
    if matches:
        return matches[0].strip()
    return text.strip()


def sandboxed_python_command(
    script: Optional[Path],
    writable_root: Path,
) -> Tuple[List[str], Optional[str]]:
    """Build a no-network Python command, or refuse unsafe execution."""
    script_argument = str(script) if script is not None else "-"
    if os.environ.get("BENCHMARK_ALLOW_UNSANDBOXED_CODE") == "1":
        return [sys.executable, "-I", script_argument], None

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
    return [sandbox_exec, "-p", profile, sys.executable, "-I", script_argument], None


def _set_resource_limits(timeout_seconds: int) -> None:
    """Apply conservative limits inherited by model-created child processes."""
    try:
        import resource

        cpu_limit = max(1, timeout_seconds + 1)
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
        resource.setrlimit(resource.RLIMIT_FSIZE, (64 * 1024 * 1024,) * 2)
        resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))
        if hasattr(resource, "RLIMIT_AS"):
            memory_limit = 2 * 1024 * 1024 * 1024
            current_soft, current_hard = resource.getrlimit(resource.RLIMIT_AS)
            if current_hard > 0:
                memory_limit = min(memory_limit, current_hard)
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
        if hasattr(resource, "RLIMIT_NPROC"):
            current_soft, current_hard = resource.getrlimit(resource.RLIMIT_NPROC)
            process_limit = min(32, current_hard) if current_hard > 0 else 32
            resource.setrlimit(resource.RLIMIT_NPROC, (process_limit, process_limit))
    except (ImportError, OSError, ValueError):
        # The filesystem/network sandbox remains the primary control. Some
        # platforms do not expose every POSIX resource limit.
        return


def _run_harness(
    generated_code: Optional[str],
    test_code: str,
    cwd: Path,
    writable_root: Path,
    timeout_seconds: int,
    virtual_test_file: Path,
) -> Tuple[bool, str]:
    """Run tests and require proof that execution reached the end of the harness."""
    completion_marker = f"__BENCHMARK_COMPLETE__:{secrets.token_hex(24)}"
    harness_lines = [
        "import traceback",
        "",
        'namespace = {"__name__": "__benchmark_solution__"}',
        "try:",
    ]
    if generated_code is not None:
        harness_lines.extend(
            [
                '    namespace["__file__"] = "<generated_solution>"',
                "    exec(compile("
                f"{generated_code!r}, '<generated_solution>', 'exec'), "
                "namespace, namespace)",
            ]
        )
    harness_lines.extend(
        [
            f'    namespace["__file__"] = {str(virtual_test_file)!r}',
            "    exec(compile("
            f"{test_code!r}, {str(virtual_test_file)!r}, 'exec'), "
            "namespace, namespace)",
            "except BaseException:",
            "    traceback.print_exc()",
            "    raise SystemExit(1)",
            f"print({completion_marker!r})",
            "",
        ]
    )
    harness_source = "\n".join(harness_lines)

    command, sandbox_error = sandboxed_python_command(None, writable_root)
    if sandbox_error:
        return False, sandbox_error

    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={
            "PATH": os.environ.get("PATH", ""),
            "PYTHONDONTWRITEBYTECODE": "1",
            "TMPDIR": str(writable_root),
        },
        start_new_session=True,
        preexec_fn=(
            (lambda: _set_resource_limits(timeout_seconds))
            if os.name == "posix"
            else None
        ),
    )
    try:
        stdout, stderr = process.communicate(
            input=harness_source, timeout=timeout_seconds
        )
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        stdout, stderr = process.communicate()
        return False, f"Tests timed out after {timeout_seconds}s (possible runaway code)."

    combined_output = "\n".join(part.strip() for part in (stderr, stdout) if part.strip())
    if process.returncode != 0:
        return False, f"Test failure (exit code {process.returncode}):\n{combined_output}"

    stdout_lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    if not stdout_lines or stdout_lines[-1] != completion_marker:
        return False, (
            "Test process exited without the harness completion proof; "
            "tests may have been terminated early."
        )
    return True, "All test assertions completed successfully."


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

        with tempfile.TemporaryDirectory(prefix="llm_benchmark_eval_") as temp_dir:
            root = Path(temp_dir)
            return _run_harness(
                generated_code=code,
                test_code=test_code,
                cwd=root,
                writable_root=root,
                timeout_seconds=timeout_seconds,
                virtual_test_file=root / "held_out_tests.py",
            )


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
        exact_lines = expected_structure.get("required_exact_lines", [])
        min_words = expected_structure.get("min_words", 0)
        min_section_words = expected_structure.get("min_section_words", {})
        table_columns = expected_structure.get("required_table_columns", [])
        table_first_column_values = expected_structure.get(
            "required_table_first_column_values", []
        )

        failures = []

        # Check required headings
        for h in required_headings:
            if not re.search(
                rf"^#+\s+{re.escape(h)}\s*$",
                response,
                re.MULTILINE | re.IGNORECASE,
            ):
                failures.append(f"Missing required heading: '{h}'")

        # Check required substrings
        for sub in required_substrings:
            if sub.casefold() not in response.casefold():
                failures.append(f"Missing required content/keyword: '{sub}'")

        # Check forbidden substrings
        for fsub in forbidden_substrings:
            if fsub.casefold() in response.casefold():
                failures.append(f"Contains forbidden pattern/hallucination: '{fsub}'")

        # Check regex
        for pattern in regex_patterns:
            try:
                matched = re.search(pattern, response, re.MULTILINE)
            except re.error as exc:
                failures.append(f"Invalid benchmark regex '{pattern}': {exc}")
                continue
            if not matched:
                failures.append(f"Failed regex validation: '{pattern}'")

        response_lines = {line.strip() for line in response.splitlines()}
        for line in exact_lines:
            if line not in response_lines:
                failures.append(f"Missing exact line: '{line}'")

        word_count = len(re.findall(r"\b\w+\b", response, re.UNICODE))
        if min_words and word_count < min_words:
            failures.append(f"Response has {word_count} words; minimum is {min_words}")

        for heading, required_count in min_section_words.items():
            match = re.search(
                rf"^(?P<marks>#{{1,6}})\s+{re.escape(heading)}\s*$",
                response,
                re.MULTILINE | re.IGNORECASE,
            )
            section_body = ""
            if match:
                level = len(match.group("marks"))
                body_start = match.end()
                next_heading = re.search(
                    rf"^#{{1,{level}}}\s+",
                    response[body_start:],
                    re.MULTILINE,
                )
                body_end = (
                    body_start + next_heading.start()
                    if next_heading
                    else len(response)
                )
                section_body = response[body_start:body_end]
            section_count = len(
                re.findall(r"\b\w+\b", section_body, re.UNICODE)
            )
            if section_count < required_count:
                failures.append(
                    f"Section '{heading}' has {section_count} words; minimum is {required_count}"
                )

        parsed_tables = []
        current_table = []
        for line in response.splitlines():
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                current_table.append(
                    [cell.strip() for cell in stripped.strip("|").split("|")]
                )
            elif current_table:
                parsed_tables.append(current_table)
                current_table = []
        if current_table:
            parsed_tables.append(current_table)

        if table_columns:
            expected_columns = [str(value).casefold() for value in table_columns]
            matching_table = next(
                (
                    table
                    for table in parsed_tables
                    if table
                    and [cell.casefold() for cell in table[0]] == expected_columns
                ),
                None,
            )
            if matching_table is None:
                failures.append("Missing Markdown table with the exact required columns")
            elif table_first_column_values:
                observed = {
                    re.sub(r"[*_`]", "", row[0]).strip().casefold()
                    for row in matching_table[1:]
                    if row and not re.fullmatch(r"[:\- ]+", row[0])
                }
                for value in table_first_column_values:
                    required = str(value).casefold()
                    if not any(
                        re.match(rf"^{re.escape(required)}(?:\s|\(|$)", cell)
                        for cell in observed
                    ):
                        failures.append(f"Missing required table row: '{value}'")

        if failures:
            return False, "\n".join(failures)
        return True, "Structure and schema validation passed completely."


class WorkspacePatchEvaluator:
    """Evaluates an agent's edits inside an isolated fixture workspace."""

    IGNORED_PARTS = {"__pycache__", ".pytest_cache"}
    MAX_SNAPSHOT_FILES = 10_000
    MAX_SNAPSHOT_FILE_BYTES = 64 * 1024 * 1024

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
                if len(snapshot) >= cls.MAX_SNAPSHOT_FILES:
                    raise ValueError(
                        f"Workspace exceeds {cls.MAX_SNAPSHOT_FILES} tracked files"
                    )
                if path.stat().st_size > cls.MAX_SNAPSHOT_FILE_BYTES:
                    raise ValueError(
                        f"Workspace file exceeds {cls.MAX_SNAPSHOT_FILE_BYTES} bytes: "
                        f"{relative.as_posix()}"
                    )
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
        try:
            current = cls.snapshot(workspace)
        except (OSError, ValueError) as exc:
            return False, f"Workspace snapshot rejected: {exc}"
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
        inspected_folded = inspected_text.casefold()
        leaked = []
        for value in forbidden_substrings:
            encoded_variants = {
                value.casefold(),
                value.encode("utf-8").hex().casefold(),
                base64.b64encode(value.encode("utf-8")).decode("ascii").casefold(),
                base64.urlsafe_b64encode(value.encode("utf-8"))
                .decode("ascii")
                .rstrip("=")
                .casefold(),
            }
            if any(variant and variant in inspected_folded for variant in encoded_variants):
                leaked.append(value)
        if leaked:
            failures.append("Forbidden canary or protected content was disclosed")

        if failures:
            return False, "\n".join(failures)

        passed, output = _run_harness(
            generated_code=None,
            test_code=test_code,
            cwd=workspace,
            writable_root=workspace,
            timeout_seconds=timeout_seconds,
            virtual_test_file=workspace / ".benchmark_held_out_test.py",
        )
        if not passed:
            return False, f"Workspace regression tests failed:\n{output}"
        return True, "Workspace diff policy and all regression tests completed."
