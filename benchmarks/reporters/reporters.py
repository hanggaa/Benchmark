from __future__ import annotations

import json
import os
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from benchmarks.models import BenchmarkResult, ModelSummary


DIFFICULTY_WEIGHTS = {"easy": 1.0, "medium": 2.0, "hard": 3.0}


def atomic_write_text(output_path: Path, content: str) -> None:
    """Replace a report atomically so interrupted runs cannot truncate it."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.", dir=output_path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, output_path)
    finally:
        temporary_path.unlink(missing_ok=True)


class JSONReporter:
    @staticmethod
    def save_report(results: List[BenchmarkResult], output_path: Path) -> None:
        data = [r.to_dict() for r in results]
        atomic_write_text(output_path, json.dumps(data, indent=2))


class MarkdownReporter:
    @staticmethod
    def generate_report(results: List[BenchmarkResult]) -> str:
        if not results:
            return "# Benchmark Report\n\nNo test results found.\n"

        # Group by (cli, model, effort)
        grouped: Dict[tuple, List[BenchmarkResult]] = defaultdict(list)
        for r in results:
            key = (r.cli, r.model, r.effort or "default")
            grouped[key].append(r)

        summaries: List[ModelSummary] = []
        cli_error_counts: Dict[tuple, int] = {}
        for (cli, model, effort), items in grouped.items():
            scored_items = [item for item in items if not item.error_message]
            cli_error_counts[(cli, model, effort)] = len(items) - len(scored_items)
            total = len(scored_items)
            passed = sum(1 for x in scored_items if x.passed)
            pass_rate = round((passed / total) * 100, 1) if total > 0 else 0.0
            total_weight = sum(
                DIFFICULTY_WEIGHTS.get(x.difficulty, 2.0) for x in scored_items
            )
            passed_weight = sum(
                DIFFICULTY_WEIGHTS.get(x.difficulty, 2.0)
                for x in scored_items
                if x.passed
            )
            weighted_pass_rate = round(
                (passed_weight / total_weight) * 100, 1
            ) if total_weight else 0.0
            avg_time = round(
                sum(x.duration_seconds for x in scored_items) / total, 2
            ) if total > 0 else 0.0
            
            total_in = sum(x.token_usage.input_tokens for x in items)
            total_out = sum(x.token_usage.output_tokens for x in items)
            total_think = sum(x.token_usage.thinking_tokens for x in items)
            total_cost = round(sum(x.token_usage.estimated_cost_usd for x in items), 6)

            # Timeout penalty to prevent artificial inflation from incomplete runs
            timeout_count = 0
            for item in scored_items:
                timeout_text = "\n".join(
                    value for value in (item.error_message, item.evaluator_logs) if value
                ).casefold()
                if "timeout" in timeout_text or "timed out" in timeout_text:
                    timeout_count += 1
            timeout_penalty = timeout_count * 0.05

            telemetry_complete = all(
                item.token_usage.telemetry_complete for item in items
            )
            # Do not rank cost efficiency when an adapter did not report complete
            # usage. Zero-valued missing telemetry previously inflated this score.
            eff_score = (
                round(
                    ((weighted_pass_rate ** 2) / 100.0)
                    / (total_cost + timeout_penalty + 0.005),
                    1,
                )
                if telemetry_complete and total > 0
                else None
            )

            summaries.append(
                ModelSummary(
                    model=model,
                    cli=cli,
                    effort=effort if effort != "default" else None,
                    total_cases=total,
                    passed_cases=passed,
                    pass_rate=pass_rate,
                    weighted_pass_rate=weighted_pass_rate,
                    avg_duration_seconds=avg_time,
                    total_input_tokens=total_in,
                    total_output_tokens=total_out,
                    total_thinking_tokens=total_think,
                    total_cost_usd=total_cost,
                    efficiency_score=eff_score,
                    telemetry_complete=telemetry_complete,
                )
            )

        summaries.sort(
            key=lambda s: (-s.weighted_pass_rate, -s.pass_rate, s.total_cost_usd)
        )

        md = []
        md.append("# 🏆 Personal LLM Benchmark Leaderboard")
        md.append("")
        total_cli_errors = sum(1 for result in results if result.error_message)
        total_scored = len(results) - total_cli_errors
        md.append(
            f"> Benchmark execution completed for **{len(summaries)}** model "
            f"configuration(s) across **{len(results)}** attempts: "
            f"**{total_scored}** scored run(s), **{total_cli_errors}** CLI error(s)."
        )
        md.append("")
        metadata = results[0].metadata
        if metadata:
            md.append("## Run Provenance")
            md.append("")
            md.append(f"- Run ID: `{metadata.get('run_id', 'unknown')}`")
            md.append(f"- Suite hash: `{metadata.get('suite_hash', 'unknown')}`")
            md.append(f"- Git commit: `{metadata.get('git_commit', 'unknown')}`")
            md.append(f"- Git working tree dirty: `{metadata.get('git_dirty', 'unknown')}`")
            md.append(f"- Python: `{metadata.get('python_version', 'unknown')}`")
            md.append(f"- Platform: `{metadata.get('platform', 'unknown')}`")
            cli_versions = metadata.get("cli_versions", {})
            if cli_versions:
                versions = ", ".join(
                    f"{cli}={version}" for cli, version in sorted(cli_versions.items())
                )
                md.append(f"- CLI versions: `{versions}`")
            md.append(f"- Config hash: `{metadata.get('config_hash', 'unknown')}`")
            if metadata.get("resumed_from_run_id"):
                md.append(
                    f"- Resumed from run ID: `{metadata['resumed_from_run_id']}`"
                )
                md.append(
                    f"- Resume root run ID: `{metadata.get('resume_root_run_id', 'unknown')}`"
                )
                md.append(
                    "- Resume results: `"
                    f"{metadata.get('reused_result_count', 0)} reused, "
                    f"{metadata.get('rerun_result_count', 0)} rerun`"
                )
                md.append(
                    "- Prior CLI-error attempts: `"
                    f"{metadata.get('prior_cli_error_attempt_count', 0)}` "
                    "(cost excluded from merged leaderboard: "
                    f"`${metadata.get('prior_cli_error_attempt_cost_usd', 0.0):.5f}`)"
                )
            pricing_metadata = metadata.get("pricing_metadata", {})
            if isinstance(pricing_metadata, dict):
                md.append(
                    "- Pricing last verified: `"
                    f"{pricing_metadata.get('last_verified_utc') or 'not recorded'}`"
                )
            md.append("")
        md.append("## 📊 Overall Model Comparison")
        md.append("")
        md.append("| Model | CLI | Effort | Pass Rate | Weighted Accuracy | CLI Errors | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |")

        for s in summaries:
            effort_str = s.effort or "-"
            key = (s.cli, s.model, s.effort or "default")
            cli_errors = cli_error_counts[key]
            pass_str = (
                f"**{s.pass_rate}%** ({s.passed_cases}/{s.total_cases})"
                if s.total_cases
                else "**N/A** (0/0)"
            )
            weighted_str = (
                f"**{s.weighted_pass_rate}%**" if s.total_cases else "**N/A**"
            )
            cost_str = f"${s.total_cost_usd:.5f}"
            efficiency_str = (
                f"**{s.efficiency_score:,.0f}**"
                if s.efficiency_score is not None
                else (
                    "N/A (no scored runs)"
                    if not s.total_cases
                    else "N/A (telemetry incomplete)"
                )
            )
            md.append(
                f"| **{s.model}** | `{s.cli}` | `{effort_str}` | {pass_str} | "
                f"{weighted_str} | {cli_errors} | {s.avg_duration_seconds}s | "
                f"{s.total_thinking_tokens:,} | {cost_str} | {efficiency_str} |"
            )

        # Category Breakdown
        categories = sorted(list(set(r.category for r in results)))
        md.append("")
        md.append("## 📂 Category Breakdown (Pass Rates)")
        md.append("")
        cat_header = ["| Model | CLI | Effort |"] + [f" {c.capitalize()} |" for c in categories]
        cat_sep = ["| :--- | :--- | :--- |"] + [" :---: |" for _ in categories]
        md.append("".join(cat_header))
        md.append("".join(cat_sep))

        for (cli, model, effort), items in grouped.items():
            row = [f"| **{model}** | `{cli}` | `{effort}` |"]
            for c in categories:
                c_attempts = [x for x in items if x.category == c]
                c_items = [x for x in c_attempts if not x.error_message]
                c_errors = len(c_attempts) - len(c_items)
                if not c_attempts:
                    row.append(" - |")
                elif not c_items:
                    row.append(f" N/A (0/0; {c_errors} CLI error) |")
                else:
                    c_pass = sum(1 for x in c_items if x.passed)
                    c_rate = round((c_pass / len(c_items)) * 100)
                    error_suffix = f"; {c_errors} CLI error" if c_errors else ""
                    row.append(
                        f" {c_rate}% ({c_pass}/{len(c_items)}{error_suffix}) |"
                    )
            md.append("".join(row))

        # Detailed Test Runs
        md.append("")
        md.append("## 📝 Detailed Test Execution Logs")
        md.append("")
        for r in results:
            status_icon = (
                "⚠️ CLI ERROR"
                if r.error_message
                else ("✅ PASS" if r.passed else "❌ FAIL")
            )
            effort_tag = f" [{r.effort}]" if r.effort else ""
            md.append(f"### {status_icon}: {r.case_title} (`{r.case_id}`)")
            md.append(f"- **Model**: `{r.model}`{effort_tag} via `{r.cli}`")
            md.append(f"- **Difficulty**: `{r.difficulty}`")
            if r.metadata.get("case_hash"):
                md.append(f"- **Case Hash**: `{r.metadata['case_hash']}`")
            md.append(f"- **Duration**: {r.duration_seconds:.2f}s")
            md.append(
                f"- **Tokens**: In: {r.token_usage.input_tokens:,} | "
                f"Out: {r.token_usage.output_tokens:,} | "
                f"Thinking: {r.token_usage.thinking_tokens:,} | "
                f"Cache Read: {r.token_usage.cache_read_tokens:,} | "
                f"Total: {r.token_usage.total_tokens:,} | "
                f"Cost: ${r.token_usage.estimated_cost_usd:.5f}"
            )
            if not r.passed:
                md.append(f"- **Error Details**:\n```\n{r.evaluator_logs or r.error_message or 'Test failed.'}\n```")
            md.append("")

        return "\n".join(md)
