from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from benchmarks.evaluators.evaluators import SchemaEvaluator, UnitTestEvaluator
from benchmarks.models import BenchmarkResult, TestCase, TokenUsage
from benchmarks.reporters.reporters import JSONReporter, MarkdownReporter
from benchmarks.runners.antigravity_runner import AntigravityRunner
from benchmarks.runners.claude_runner import ClaudeRunner
from benchmarks.runners.codex_runner import CodexRunner
from benchmarks.runners.opencode_runner import OpenCodeRunner


def load_config() -> Dict[str, Any]:
    config_path = Path(__file__).parent / "config.json"
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def load_test_cases(
    categories: Optional[List[str]] = None,
    case_ids: Optional[List[str]] = None,
) -> List[TestCase]:
    cases_dir = Path(__file__).parent / "cases"
    case_files = glob.glob(str(cases_dir / "**" / "*.json"), recursive=True)
    test_cases: List[TestCase] = []

    for fpath in sorted(case_files):
        try:
            data = json.loads(Path(fpath).read_text(encoding="utf-8"))
            tc = TestCase(
                id=data["id"],
                title=data["title"],
                category=data["category"],
                description=data.get("description", ""),
                prompt=data["prompt"],
                evaluator_type=data["evaluator_type"],
                test_code=data.get("test_code", ""),
                expected_structure=data.get("expected_structure", {}),
                timeout_seconds=data.get("timeout_seconds", 120),
                difficulty=data.get("difficulty", "medium"),
            )

            if categories and tc.category not in categories:
                continue
            if case_ids and tc.id not in case_ids:
                continue

            test_cases.append(tc)
        except Exception as e:
            print(f"[WARN] Failed to load case file {fpath}: {e}")

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

    # Fallback to first CLI requested
    return requested_clis[0] if requested_clis else "agy"


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


def run_benchmark(
    clis: List[str],
    models: List[str],
    effort: Optional[str] = None,
    categories: Optional[List[str]] = None,
    case_ids: Optional[List[str]] = None,
    timeout_override: Optional[int] = None,
    output_dir: Optional[str] = None,
    dry_run: bool = False,
) -> List[BenchmarkResult]:
    config = load_config()
    test_cases = load_test_cases(categories, case_ids)

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
    timeout_display = f"• Global Timeout: {timeout_override}s\n" if timeout_override else ""
    print(f"• Test Cases: {len(test_cases)} case(s)")
    if timeout_display:
        print(timeout_display, end="")
    print("=" * 70)

    results: List[BenchmarkResult] = []
    runners_cache: Dict[str, Any] = {}

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

            if dry_run:
                time.sleep(0.05)
                print("⏩ SKIPPED (Dry Run)")
                continue

            current_timeout = timeout_override or tc.timeout_seconds

            resp, tokens, duration, err = runner.run_prompt(
                prompt=tc.prompt,
                model=model,
                effort=model_effort,
                timeout_seconds=current_timeout,
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
                    )
                )
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
            else:
                eval_passed = True
                eval_logs = "No specific evaluator defined."

            status_icon = "✅ PASS" if eval_passed else "❌ FAIL"
            print(
                f"{status_icon} ({duration:.1f}s | In: {tokens.input_tokens:,} | Out: {tokens.output_tokens:,} | Think: {tokens.thinking_tokens:,} | ${tokens.estimated_cost_usd:.5f})"
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
                )
            )

    # Generate and save reports
    out_path = Path(output_dir) if output_dir else Path(__file__).parent / "reports"
    out_path.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    md_report = MarkdownReporter.generate_report(results)
    md_file = out_path / f"benchmark_report_{timestamp}.md"
    md_file.write_text(md_report, encoding="utf-8")

    json_file = out_path / f"benchmark_data_{timestamp}.json"
    JSONReporter.save_report(results, json_file)

    latest_md = out_path / "latest_report.md"
    latest_md.write_text(md_report, encoding="utf-8")

    # Also save to frontend web data folder
    web_data_file = Path(__file__).parent.parent / "src" / "data" / "benchmark-data.json"
    web_data_file.parent.mkdir(parents=True, exist_ok=True)
    JSONReporter.save_report(results, web_data_file)

    print("\n" + "=" * 70)
    print("🎉 BENCHMARK RUN COMPLETE!")
    print(f"📄 Latest Report Saved to: {latest_md}")
    print(f"📄 Full JSON Data Saved to: {json_file}")
    print("=" * 70)
    print("\n" + md_report)

    return results


def main():
    parser = argparse.ArgumentParser(description="Personal LLM Benchmark Suite for Coding & Agentic CLIs")
    parser.add_argument("--cli", default="auto", help="Target CLI (agy, claude, codex, opencode, auto) or comma-separated list")
    parser.add_argument("--models", required=True, help="Comma-separated model names (e.g. 'Gemini 3.7 Flash (High), gpt-5.6-sol --effort high')")
    parser.add_argument("--effort", default=None, help="Reasoning effort (low, medium, high)")
    parser.add_argument("--category", default=None, help="Filter by category (logic, bugfix, research, tool_use)")
    parser.add_argument("--case", default=None, help="Filter by specific case ID")
    parser.add_argument("--timeout", type=int, default=None, help="Global timeout limit in seconds (e.g. 300, 360, 480)")
    parser.add_argument("--output-dir", default=None, help="Output directory for reports")
    parser.add_argument("--dry-run", action="store_true", help="List test cases without executing LLM calls")

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
    )


if __name__ == "__main__":
    main()
