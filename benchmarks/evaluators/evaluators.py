from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple


def extract_python_code(text: str) -> str:
    """Extracts the first valid python code block or returns the text if no code fence."""
    pattern = r"```(?:python|py)?\s*\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return max(matches, key=len).strip()
    return text.strip()


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

        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False, encoding="utf-8") as f:
            f.write(full_script)
            temp_path = f.name

        try:
            res = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
            if res.returncode == 0:
                return True, "All test assertions passed successfully."
            else:
                err_output = (res.stderr or res.stdout).strip()
                return False, f"Test failure (exit code {res.returncode}):\n{err_output}"
        except subprocess.TimeoutExpired:
            return False, f"Unit tests timed out after {timeout_seconds}s (possible infinite loop)."
        except Exception as exc:
            return False, f"Evaluation execution error: {exc}"
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


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
