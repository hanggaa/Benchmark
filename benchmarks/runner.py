from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from benchmarks.evaluators.evaluators import (
    SchemaEvaluator,
    UnitTestEvaluator,
    WorkspacePatchEvaluator,
)
from benchmarks.models import BenchmarkResult, TestCase, TokenUsage
from benchmarks.reporters.reporters import JSONReporter, MarkdownReporter, atomic_write_text
from benchmarks.runners.antigravity_runner import AntigravityRunner
from benchmarks.runners.claude_runner import ClaudeRunner
from benchmarks.runners.codex_runner import CodexRunner
from benchmarks.runners.opencode_runner import OpenCodeRunner


SUPPORTED_EVALUATORS = {"python_unit_test", "schema_check", "workspace_patch_test"}
SUPPORTED_DIFFICULTIES = {"easy", "medium", "hard"}


def hash_workspace_fixture(fixture: Path) -> str:
    """Hash stable fixture inputs while rejecting links outside the fixture."""
    digest = hashlib.sha256()
    for path in sorted(fixture.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(fixture)
        if "__pycache__" in relative.parts or path.suffix == ".pyc":
            continue
        if path.name == ".DS_Store":
            continue
        if path.is_symlink():
            raise BenchmarkConfigurationError(
                f"workspace fixture must not contain symlinks: {relative}"
            )
        if not path.is_file():
            continue
        relative_bytes = relative.as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative_bytes).to_bytes(8, "big"))
        digest.update(relative_bytes)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


class BenchmarkConfigurationError(ValueError):
    """Raised when a benchmark case or run is not reproducible or safe."""


def load_config() -> Dict[str, Any]:
    config_path = Path(__file__).parent / "config.json"
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def load_test_cases(
    categories: Optional[List[str]] = None,
    case_ids: Optional[List[str]] = None,
    private_tests_dir: Optional[str] = None,
) -> List[TestCase]:
    cases_dir = Path(__file__).parent / "cases"
    case_files = sorted(cases_dir.rglob("*.json"))
    test_cases: List[TestCase] = []
    errors: List[str] = []
    seen_ids: Dict[str, Path] = {}

    configured_private_dir = private_tests_dir or os.environ.get(
        "BENCHMARK_PRIVATE_TESTS_DIR"
    )
    private_root = (
        Path(configured_private_dir).expanduser().resolve()
        if configured_private_dir
        else None
    )
    if private_root is not None and not private_root.is_dir():
        raise BenchmarkConfigurationError(
            f"Private tests directory does not exist: {private_root}"
        )

    for fpath in sorted(case_files):
        try:
            raw_case = fpath.read_text(encoding="utf-8")
            data = json.loads(raw_case)
            if not isinstance(data, dict):
                raise BenchmarkConfigurationError("top-level JSON must be an object")

            for key in ("id", "title", "category", "prompt", "evaluator_type"):
                if not isinstance(data.get(key), str) or not data[key].strip():
                    raise BenchmarkConfigurationError(
                        f"'{key}' must be a non-empty string"
                    )

            case_id = data["id"]
            if case_id in seen_ids:
                raise BenchmarkConfigurationError(
                    f"duplicate id '{case_id}' also used by {seen_ids[case_id]}"
                )
            seen_ids[case_id] = fpath

            evaluator_type = data["evaluator_type"]
            if evaluator_type not in SUPPORTED_EVALUATORS:
                raise BenchmarkConfigurationError(
                    f"unsupported evaluator_type '{evaluator_type}'"
                )

            difficulty = data.get("difficulty", "medium")
            if difficulty not in SUPPORTED_DIFFICULTIES:
                raise BenchmarkConfigurationError(
                    f"difficulty must be one of {sorted(SUPPORTED_DIFFICULTIES)}"
                )

            timeout_seconds = data.get("timeout_seconds", 120)
            if (
                not isinstance(timeout_seconds, int)
                or isinstance(timeout_seconds, bool)
                or timeout_seconds <= 0
            ):
                raise BenchmarkConfigurationError(
                    "timeout_seconds must be a positive integer"
                )

            list_fields = (
                "allowed_changed_files",
                "required_changed_files",
                "forbidden_substrings",
            )
            for key in list_fields:
                value = data.get(key, [])
                if not isinstance(value, list) or not all(
                    isinstance(item, str) for item in value
                ):
                    raise BenchmarkConfigurationError(
                        f"'{key}' must be a list of strings"
                    )

            expected_structure = data.get("expected_structure", {})
            if not isinstance(expected_structure, dict):
                raise BenchmarkConfigurationError(
                    "expected_structure must be an object"
                )
            schema_list_fields = (
                "required_headings",
                "required_substrings",
                "forbidden_substrings",
                "regex_patterns",
                "required_exact_lines",
                "required_table_columns",
                "required_table_first_column_values",
            )
            for key in schema_list_fields:
                value = expected_structure.get(key, [])
                if not isinstance(value, list) or not all(
                    isinstance(item, str) for item in value
                ):
                    raise BenchmarkConfigurationError(
                        f"expected_structure.{key} must be a list of strings"
                    )
            min_words = expected_structure.get("min_words", 0)
            if (
                not isinstance(min_words, int)
                or isinstance(min_words, bool)
                or min_words < 0
            ):
                raise BenchmarkConfigurationError(
                    "expected_structure.min_words must be a non-negative integer"
                )
            section_words = expected_structure.get("min_section_words", {})
            if not isinstance(section_words, dict) or not all(
                isinstance(key, str)
                and isinstance(value, int)
                and not isinstance(value, bool)
                and value >= 0
                for key, value in section_words.items()
            ):
                raise BenchmarkConfigurationError(
                    "expected_structure.min_section_words must map headings to "
                    "non-negative integers"
                )
            for pattern in expected_structure.get("regex_patterns", []):
                re.compile(pattern)

            test_code = data.get("test_code", "")
            test_source = "inline-public"
            if private_root is not None:
                private_test = (private_root / f"{case_id}.py").resolve()
                if private_root != private_test and private_root not in private_test.parents:
                    raise BenchmarkConfigurationError("private test path escaped its root")
                if private_test.is_file():
                    test_code = private_test.read_text(encoding="utf-8")
                    test_source = "private"

            if evaluator_type in {"python_unit_test", "workspace_patch_test"}:
                if not isinstance(test_code, str) or not test_code.strip():
                    raise BenchmarkConfigurationError(
                        "executable evaluators require non-empty test code"
                    )
            if evaluator_type == "schema_check" and not expected_structure:
                raise BenchmarkConfigurationError(
                    "schema_check requires expected_structure"
                )
            fixture_hash = ""
            if evaluator_type == "workspace_patch_test":
                if not data.get("workspace_fixture"):
                    raise BenchmarkConfigurationError(
                        "workspace_patch_test requires workspace_fixture"
                    )
                if not data.get("allowed_changed_files"):
                    raise BenchmarkConfigurationError(
                        "workspace_patch_test requires allowed_changed_files"
                    )
                fixtures_root = (Path(__file__).parent / "fixtures").resolve()
                fixture = (Path(__file__).parent / data["workspace_fixture"]).resolve()
                if (
                    fixture == fixtures_root
                    or fixtures_root not in fixture.parents
                    or not fixture.is_dir()
                ):
                    raise BenchmarkConfigurationError(
                        f"workspace fixture is invalid or not found: {fixture}"
                    )
                fixture_hash = hash_workspace_fixture(fixture)

            canonical_case = json.dumps(
                data, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            )
            case_hash = hashlib.sha256(
                (
                    canonical_case
                    + "\n"
                    + test_code
                    + "\nfixture:"
                    + fixture_hash
                ).encode("utf-8")
            ).hexdigest()
            tc = TestCase(
                id=case_id,
                title=data["title"],
                category=data["category"],
                description=data.get("description", ""),
                prompt=data["prompt"],
                evaluator_type=evaluator_type,
                test_code=test_code,
                expected_structure=expected_structure,
                timeout_seconds=timeout_seconds,
                difficulty=difficulty,
                workspace_fixture=data.get("workspace_fixture", ""),
                allowed_changed_files=data.get("allowed_changed_files", []),
                required_changed_files=data.get("required_changed_files", []),
                forbidden_substrings=data.get("forbidden_substrings", []),
                source_path=str(fpath.relative_to(Path(__file__).parent.parent)),
                case_hash=case_hash,
                fixture_hash=fixture_hash,
                test_source=test_source,
            )

            if categories and tc.category not in categories:
                continue
            if case_ids and tc.id not in case_ids:
                continue

            test_cases.append(tc)
        except Exception as exc:
            errors.append(f"{fpath}: {exc}")

    if errors:
        raise BenchmarkConfigurationError(
            "Invalid benchmark case configuration:\n- " + "\n- ".join(errors)
        )

    return test_cases


def get_runner(cli_name: str, config: Dict[str, Any]):
    cli_lower = cli_name.lower().strip()
    if cli_lower in ("agy", "antigravity"):
        return AntigravityRunner(config)
    elif cli_lower in ("claude", "claude-code"):
        return ClaudeRunner(config)
    elif cli_lower in ("codex", "codex-cli"):
        return CodexRunner(config)
    elif cli_lower in ("opencode", "open-code"):
        return OpenCodeRunner(config)
    else:
        raise ValueError(f"Unsupported CLI adapter: {cli_name}. Supported: agy, claude, codex, opencode")


def infer_cli_for_model(model_name: str, requested_clis: List[str]) -> str:
    """Smart auto-routing: maps model names to their native CLI adapter."""
    m = model_name.lower().strip()

    # Explicit prefix like "codex:gpt-5.6-sol" or "agy:Gemini 3.7"
    for prefix in ("agy:", "codex:", "opencode:", "claude:"):
        if m.startswith(prefix):
            return prefix[:-1]

    # OpenCode models (often provider/model format or bailian/qwen/deepseek)
    if m.startswith("opencode/") or m.startswith("bailian-") or m.startswith("ollama/") or "deepseek" in m or "qwen" in m:
        return "opencode"

    # OpenAI / Codex models
    if m.startswith("gpt-") or m.startswith("o1") or m.startswith("o3") or "chatgpt" in m:
        return "codex"

    # Anthropic / Claude Code models
    if "claude" in m and not ("opencode" in requested_clis and len(requested_clis) == 1):
        if "claude" in requested_clis:
            return "claude"
        elif "agy" in requested_clis:
            return "agy"
        return "claude"

    # Google / Gemini models
    if "gemini" in m:
        return "agy"

    # Fallback only when the caller supplied a concrete adapter. Guessing an
    # adapter for an unknown model makes the resulting comparison ambiguous.
    concrete_clis = [cli for cli in requested_clis if cli not in ("auto", "all")]
    if concrete_clis:
        return concrete_clis[0]
    raise BenchmarkConfigurationError(
        f"Cannot infer a CLI adapter for model '{model_name}'. Use cli:model."
    )


def parse_model_spec(raw_spec: str, global_effort: Optional[str] = None, default_cli: Optional[str] = None) -> Tuple[str, str, Optional[str]]:
    """
    Parses strings like:
      - "Gemini 3.7 Flash (High)"
      - "gpt-5.6-sol --effort high"
      - "codex:gpt-5.6-sol:high"
      - "opencode:opencode/deepseek-v4-flash-free"
    Returns (cli, clean_model, effort)
    """
    spec = " ".join(raw_spec.split()).strip()
    cli = default_cli or ""
    effort = global_effort

    # Check for CLI prefix (e.g. agy:..., codex:...)
    if ":" in spec and not spec.startswith("http"):
        parts = spec.split(":", 1)
        if parts[0].lower() in ("agy", "codex", "opencode", "claude", "antigravity"):
            cli = parts[0].lower()
            spec = parts[1].strip()

    # Optional trailing effort in cli:model:effort syntax. Restrict the suffix
    # to known effort names so provider-specific model tags remain untouched.
    effort_match = re.match(r"^(.*):(low|medium|high|max|xhigh|ultra)$", spec, re.I)
    if effort_match:
        spec = effort_match.group(1).strip()
        effort = effort_match.group(2).lower()

    # Check for embedded --effort in string
    if " --effort " in spec:
        m_parts = spec.split(" --effort ")
        spec = m_parts[0].strip()
        effort = m_parts[1].strip()

    # Check for (High), (Medium), (Low) in model name
    if not effort:
        if "(High)" in spec or "(high)" in spec:
            effort = "high"
        elif "(Medium)" in spec or "(medium)" in spec:
            effort = "medium"
        elif "(Low)" in spec or "(low)" in spec:
            effort = "low"

    return cli, spec, effort


def _git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=3,
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def _git_is_dirty() -> Optional[bool]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=3,
        )
        return bool(result.stdout.strip()) if result.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def _cli_version(cli_name: str) -> str:
    binary = {
        "antigravity": "agy",
        "agy": "agy",
        "claude-code": "claude",
        "claude": "claude",
        "codex-cli": "codex",
        "codex": "codex",
        "open-code": "opencode",
        "opencode": "opencode",
    }.get(cli_name, cli_name)
    if not shutil.which(binary):
        return "not-installed"
    try:
        result = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        output = (result.stdout or result.stderr).strip().splitlines()
        return output[0] if result.returncode == 0 and output else "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def _run_metadata(
    test_cases: List[TestCase], execution_plan: List[Tuple[str, str, Optional[str]]]
) -> Dict[str, Any]:
    config = load_config()
    suite_material = "\n".join(
        f"{case.id}:{case.case_hash}" for case in sorted(test_cases, key=lambda c: c.id)
    )
    return {
        "run_id": str(uuid.uuid4()),
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "suite_hash": hashlib.sha256(suite_material.encode("utf-8")).hexdigest(),
        "case_count": len(test_cases),
        "git_commit": _git_commit(),
        "git_dirty": _git_is_dirty(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "cli_versions": {
            cli: _cli_version(cli) for cli in sorted({item[0] for item in execution_plan})
        },
        "config_hash": hashlib.sha256(
            json.dumps(config, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        ).hexdigest(),
        "pricing_metadata": config.get("pricing_metadata", {}),
    }


def _result_key(
    cli: str, model: str, effort: Optional[str], case_id: str
) -> Tuple[str, str, Optional[str], str]:
    return cli, model, effort, case_id


def _load_resume_results(
    resume_from: str,
    test_cases: List[TestCase],
    execution_plan: List[Tuple[str, str, Optional[str]]],
    run_metadata: Dict[str, Any],
) -> Tuple[Dict[Tuple[str, str, Optional[str], str], BenchmarkResult], Dict[str, Any]]:
    """Load compatible successful results and identify prior CLI errors to rerun."""
    source_path = Path(resume_from).expanduser().resolve()
    try:
        raw_results = json.loads(source_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BenchmarkConfigurationError(
            f"Cannot read resume report '{source_path}': {exc}"
        ) from exc
    if not isinstance(raw_results, list) or not raw_results:
        raise BenchmarkConfigurationError(
            "Resume report must be a non-empty JSON result list."
        )

    try:
        source_results = [BenchmarkResult.from_dict(item) for item in raw_results]
    except (TypeError, ValueError) as exc:
        raise BenchmarkConfigurationError(f"Invalid resume report: {exc}") from exc

    expected_keys = {
        _result_key(cli, model, model_effort, tc.id)
        for cli, model, model_effort in execution_plan
        for tc in test_cases
    }
    source_by_key: Dict[Tuple[str, str, Optional[str], str], BenchmarkResult] = {}
    for result in source_results:
        key = _result_key(result.cli, result.model, result.effort, result.case_id)
        if key in source_by_key:
            raise BenchmarkConfigurationError(
                f"Resume report contains duplicate result: {key}."
            )
        source_by_key[key] = result
    if set(source_by_key) != expected_keys:
        raise BenchmarkConfigurationError(
            "Resume report does not contain exactly the requested models and cases."
        )

    source_metadata = source_results[0].metadata
    if not isinstance(source_metadata, dict):
        raise BenchmarkConfigurationError("Resume report metadata must be an object.")
    for field in ("suite_hash", "config_hash"):
        if source_metadata.get(field) != run_metadata.get(field):
            raise BenchmarkConfigurationError(
                f"Resume report {field} does not match the current benchmark."
            )
    case_hashes = {tc.id: tc.case_hash for tc in test_cases}
    for result in source_results:
        if result.metadata.get("case_hash") != case_hashes[result.case_id]:
            raise BenchmarkConfigurationError(
                f"Resume report case hash is stale for {result.case_id}."
            )

    reusable = {
        key: result for key, result in source_by_key.items() if not result.error_message
    }
    prior_errors = [result for result in source_results if result.error_message]
    resume_metadata = {
        "resumed_from_path": str(source_path),
        "resumed_from_run_id": source_metadata.get("run_id", "unknown"),
        "resume_root_run_id": source_metadata.get(
            "resume_root_run_id", source_metadata.get("run_id", "unknown")
        ),
        "resume_chain_depth": source_metadata.get("resume_chain_depth", 0) + 1,
        "reused_result_count": len(reusable),
        "rerun_result_count": len(prior_errors),
        "prior_cli_error_attempt_count": (
            source_metadata.get("prior_cli_error_attempt_count", 0)
            + len(prior_errors)
        ),
        "prior_cli_error_attempt_cost_usd": round(
            source_metadata.get("prior_cli_error_attempt_cost_usd", 0.0)
            + sum(result.token_usage.estimated_cost_usd for result in prior_errors),
            6,
        ),
    }
    return reusable, resume_metadata


def run_benchmark(
    clis: List[str],
    models: List[str],
    effort: Optional[str] = None,
    categories: Optional[List[str]] = None,
    case_ids: Optional[List[str]] = None,
    timeout_override: Optional[int] = None,
    output_dir: Optional[str] = None,
    dry_run: bool = False,
    publish: bool = False,
    private_tests_dir: Optional[str] = None,
    resume_from: Optional[str] = None,
) -> List[BenchmarkResult]:
    config = load_config()
    test_cases = load_test_cases(categories, case_ids, private_tests_dir)

    if publish and (categories or case_ids):
        raise BenchmarkConfigurationError(
            "Refusing to publish a filtered run. Remove --category/--case."
        )
    if dry_run and resume_from:
        raise BenchmarkConfigurationError(
            "--resume-from cannot be combined with --dry-run."
        )

    if not test_cases:
        print("❌ No matching test cases found.")
        return []

    # Build execution plan with smart model-to-CLI pairing
    execution_plan: List[Tuple[str, str, Optional[str]]] = []
    
    # If user passed a single CLI and didn't prefix models, run all on that CLI
    # Otherwise, smartly pair each model to its native CLI
    single_cli_mode = len(clis) == 1 and clis[0] not in ("auto", "all")

    for raw_m in models:
        c_cli, c_model, c_effort = parse_model_spec(raw_m, global_effort=effort)
        
        if not c_cli:
            if single_cli_mode:
                c_cli = clis[0]
            else:
                c_cli = infer_cli_for_model(c_model, clis)
                
        execution_plan.append((c_cli, c_model, c_effort))

    print("=" * 70)
    print(f"🚀 STARTING LLM BENCHMARK SUITE")
    print(f"• Execution Plan ({len(execution_plan)} target models):")
    for c_cli, c_model, c_effort in execution_plan:
        effort_str = f" [Effort: {c_effort}]" if c_effort else ""
        print(f"   ↳ Model: '{c_model}'{effort_str} via CLI: '{c_cli}'")
    timeout_display = (
        f"• Per-case Timeout Override: {timeout_override}s\n"
        if timeout_override
        else ""
    )
    print(f"• Test Cases: {len(test_cases)} case(s)")
    if timeout_display:
        print(timeout_display, end="")
    print("=" * 70)

    if dry_run:
        for tc in test_cases:
            print(
                f"⏩ {tc.id} [{tc.difficulty}] via {tc.evaluator_type} "
                f"(tests: {tc.test_source})"
            )
        print("Dry run complete; no model calls or report files were created.")
        return []

    results: List[BenchmarkResult] = []
    runners_cache: Dict[str, Any] = {}
    run_metadata = _run_metadata(test_cases, execution_plan)
    reusable_results: Dict[
        Tuple[str, str, Optional[str], str], BenchmarkResult
    ] = {}
    if resume_from:
        reusable_results, resume_metadata = _load_resume_results(
            resume_from, test_cases, execution_plan, run_metadata
        )
        run_metadata.update(resume_metadata)
        print(
            f"• Resume: reusing {len(reusable_results)} result(s), rerunning "
            f"{resume_metadata['rerun_result_count']} CLI error(s)."
        )

    def metadata_for(tc: TestCase) -> Dict[str, Any]:
        return {
            **run_metadata,
            "case_hash": tc.case_hash,
            "fixture_hash": tc.fixture_hash or None,
            "case_source": tc.source_path,
            "test_source": tc.test_source,
        }

    for cli_name, model, model_effort in execution_plan:
        if cli_name not in runners_cache:
            try:
                runners_cache[cli_name] = get_runner(cli_name, config)
            except ValueError as exc:
                print(f"❌ {exc}")
                continue

        runner = runners_cache[cli_name]
        effort_label = model_effort or "default"
        print(f"\n⚡ Testing Model: [{model}] on CLI: [{cli_name}] (Effort: {effort_label})")
        print("-" * 70)

        for idx, tc in enumerate(test_cases, 1):
            print(f"[{idx}/{len(test_cases)}] Running: {tc.title} ({tc.id})... ", end="", flush=True)

            result_key = _result_key(cli_name, model, model_effort, tc.id)
            if result_key in reusable_results:
                reused = reusable_results[result_key]
                origin_run_id = reused.metadata.get("run_id", "unknown")
                reused.metadata = {
                    **metadata_for(tc),
                    "result_origin_run_id": origin_run_id,
                    "result_reused": True,
                }
                results.append(reused)
                print("♻️ REUSED")
                continue

            if tc.evaluator_type not in SUPPORTED_EVALUATORS:
                eval_logs = f"Unknown evaluator type: {tc.evaluator_type}"
                print("❌ FAIL (invalid benchmark configuration)")
                results.append(
                    BenchmarkResult(
                        case_id=tc.id,
                        case_title=tc.title,
                        category=tc.category,
                        model=model,
                        cli=cli_name,
                        passed=False,
                        duration_seconds=0.0,
                        token_usage=TokenUsage(),
                        evaluator_logs=eval_logs,
                        effort=model_effort,
                        difficulty=tc.difficulty,
                        metadata=metadata_for(tc),
                    )
                )
                continue

            current_timeout = timeout_override or tc.timeout_seconds

            temp_workspace = None
            workspace = None
            baseline = None
            if tc.evaluator_type == "workspace_patch_test":
                fixtures_root = (Path(__file__).parent / "fixtures").resolve()
                fixture = (Path(__file__).parent / tc.workspace_fixture).resolve()
                fixture_is_safe = (
                    fixture != fixtures_root and fixtures_root in fixture.parents
                )
                if not fixture_is_safe or not fixture.is_dir():
                    err = f"Workspace fixture is invalid or not found: {fixture}"
                    resp, tokens, duration = "", TokenUsage(), 0.0
                else:
                    temp_workspace = tempfile.TemporaryDirectory(
                        prefix=f"benchmark_{tc.id}_"
                    )
                    workspace = Path(temp_workspace.name) / "workspace"
                    shutil.copytree(fixture, workspace)
                    baseline = WorkspacePatchEvaluator.snapshot(workspace)
                    resp, tokens, duration, err = runner.run_prompt(
                        prompt=tc.prompt,
                        model=model,
                        effort=model_effort,
                        timeout_seconds=current_timeout,
                        cwd=str(workspace),
                        workspace_mode=True,
                    )
            else:
                # Never expose the repository as the CLI working directory for
                # response-only cases. This keeps held-out tests and unrelated
                # project context outside the agent's execution workspace.
                with tempfile.TemporaryDirectory(
                    prefix=f"benchmark_prompt_{tc.id}_"
                ) as prompt_workspace:
                    resp, tokens, duration, err = runner.run_prompt(
                        prompt=tc.prompt,
                        model=model,
                        effort=model_effort,
                        timeout_seconds=current_timeout,
                        cwd=prompt_workspace,
                        workspace_mode=False,
                    )

            if err:
                print(f"❌ CLI ERROR ({duration:.1f}s)")
                if err:
                    print(f"     ↳ {err.strip().splitlines()[0]}")
                results.append(
                    BenchmarkResult(
                        case_id=tc.id,
                        case_title=tc.title,
                        category=tc.category,
                        model=model,
                        cli=cli_name,
                        passed=False,
                        duration_seconds=duration,
                        token_usage=tokens,
                        error_message=err,
                        effort=model_effort,
                        difficulty=tc.difficulty,
                        metadata=metadata_for(tc),
                    )
                )
                if temp_workspace is not None:
                    temp_workspace.cleanup()
                continue

            # Run evaluator
            eval_passed = False
            eval_logs = ""

            if tc.evaluator_type == "python_unit_test":
                eval_passed, eval_logs = UnitTestEvaluator.evaluate(
                    resp, tc.test_code, timeout_seconds=15
                )
            elif tc.evaluator_type == "schema_check":
                eval_passed, eval_logs = SchemaEvaluator.evaluate(
                    resp, tc.expected_structure
                )
            elif tc.evaluator_type == "workspace_patch_test":
                if workspace is None or baseline is None:
                    eval_passed = False
                    eval_logs = "Workspace fixture was not prepared."
                else:
                    eval_passed, eval_logs = WorkspacePatchEvaluator.evaluate(
                        resp,
                        workspace,
                        baseline,
                        tc.test_code,
                        tc.allowed_changed_files,
                        tc.required_changed_files,
                        tc.forbidden_substrings,
                        timeout_seconds=min(current_timeout, 60),
                    )
            else:
                eval_passed = False
                eval_logs = f"Unknown evaluator type: {tc.evaluator_type}"

            if temp_workspace is not None:
                temp_workspace.cleanup()

            status_icon = "✅ PASS" if eval_passed else "❌ FAIL"
            print(
                f"{status_icon} ({duration:.1f}s | In: {tokens.input_tokens:,} | "
                f"Out: {tokens.output_tokens:,} | Think: {tokens.thinking_tokens:,} | "
                f"Cache: {tokens.cache_read_tokens:,} | Total: {tokens.total_tokens:,} | "
                f"${tokens.estimated_cost_usd:.5f})"
            )

            if not eval_passed and eval_logs:
                for line in eval_logs.strip().splitlines()[:3]:
                    print(f"     ↳ {line}")

            results.append(
                BenchmarkResult(
                    case_id=tc.id,
                    case_title=tc.title,
                    category=tc.category,
                    model=model,
                    cli=cli_name,
                    passed=eval_passed,
                    duration_seconds=duration,
                    token_usage=tokens,
                    raw_response=resp,
                    evaluator_logs=eval_logs,
                    effort=model_effort,
                    difficulty=tc.difficulty,
                    metadata=metadata_for(tc),
                )
            )

    if not results:
        print("No benchmark results were produced; no reports were written.")
        return []

    # Generate and save reports
    out_path = Path(output_dir) if output_dir else Path(__file__).parent / "reports"
    out_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")

    md_report = MarkdownReporter.generate_report(results)
    md_file = out_path / f"benchmark_report_{timestamp}.md"
    atomic_write_text(md_file, md_report)

    json_file = out_path / f"benchmark_data_{timestamp}.json"
    JSONReporter.save_report(results, json_file)

    if publish:
        expected_results = len(test_cases) * len(execution_plan)
        if len(results) != expected_results:
            raise BenchmarkConfigurationError(
                "Refusing to publish an incomplete run: "
                f"expected {expected_results} results, received {len(results)}."
            )
        cli_errors = [result for result in results if result.error_message]
        if cli_errors:
            examples = ", ".join(
                f"{result.model}/{result.case_id}" for result in cli_errors[:3]
            )
            raise BenchmarkConfigurationError(
                "Refusing to publish a run containing "
                f"{len(cli_errors)} CLI/infrastructure error(s): {examples}."
            )
        latest_md = out_path / "latest_report.md"
        atomic_write_text(latest_md, md_report)
        web_data_file = Path(__file__).parent.parent / "src" / "data" / "benchmark-data.json"
        web_data_file.parent.mkdir(parents=True, exist_ok=True)
        JSONReporter.save_report(results, web_data_file)

    print("\n" + "=" * 70)
    print("🎉 BENCHMARK RUN COMPLETE!")
    print(f"📄 Markdown Report Saved to: {md_file}")
    print(f"📄 Full JSON Data Saved to: {json_file}")
    if publish:
        print(f"📄 Published Latest Report: {latest_md}")
    print(f"🌐 Dashboard Published: {'yes' if publish else 'no'}")
    print("=" * 70)
    print("\n" + md_report)

    return results


def main():
    parser = argparse.ArgumentParser(description="Personal LLM Benchmark Suite for Coding & Agentic CLIs")
    parser.add_argument("--cli", default="auto", help="Target CLI (agy, claude, codex, opencode, auto) or comma-separated list")
    parser.add_argument("--models", required=True, help="Comma-separated model names (e.g. 'Gemini 3.7 Flash (High), gpt-5.6-sol --effort high')")
    parser.add_argument("--effort", default=None, help="Reasoning effort (low, medium, high)")
    parser.add_argument("--category", default=None, help="Filter by category (for example: logic, security, stateful_systems, agentic_repo)")
    parser.add_argument("--case", default=None, help="Filter by specific case ID")
    parser.add_argument("--timeout", type=int, default=None, help="Global timeout limit in seconds (e.g. 300, 360, 480)")
    parser.add_argument("--output-dir", default=None, help="Output directory for reports")
    parser.add_argument("--dry-run", action="store_true", help="List test cases without executing LLM calls")
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish a complete, unfiltered run to the web dashboard",
    )
    parser.add_argument(
        "--private-tests-dir",
        default=None,
        help="Optional directory containing private <case_id>.py overrides",
    )
    parser.add_argument(
        "--resume-from",
        default=None,
        help="Reuse scored results from a compatible JSON report and rerun only CLI errors",
    )

    args = parser.parse_args()

    clis = [c.strip() for c in args.cli.split(",") if c.strip()]
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    categories = [c.strip() for c in args.category.split(",")] if args.category else None
    case_ids = [c.strip() for c in args.case.split(",")] if args.case else None

    run_benchmark(
        clis=clis,
        models=models,
        effort=args.effort,
        categories=categories,
        case_ids=case_ids,
        timeout_override=args.timeout,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
        publish=args.publish,
        private_tests_dir=args.private_tests_dir,
        resume_from=args.resume_from,
    )


if __name__ == "__main__":
    main()
