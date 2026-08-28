from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from benchmarks.models import BenchmarkResult, ModelSummary


class JSONReporter:
    @staticmethod
    def save_report(results: List[BenchmarkResult], output_path: Path) -> None:
        data = [r.to_dict() for r in results]
        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


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
        for (cli, model, effort), items in grouped.items():
            total = len(items)
            passed = sum(1 for x in items if x.passed)
            pass_rate = round((passed / total) * 100, 1) if total > 0 else 0.0
            avg_time = round(sum(x.duration_seconds for x in items) / total, 2) if total > 0 else 0.0
            
            total_in = sum(x.token_usage.input_tokens for x in items)
            total_out = sum(x.token_usage.output_tokens for x in items)
            total_think = sum(x.token_usage.thinking_tokens for x in items)
            total_cost = round(sum(x.token_usage.estimated_cost_usd for x in items), 6)

            # Timeout penalty to prevent artificial inflation from incomplete runs
            timeout_count = sum(
                1 for x in items 
                if "TIMEOUT" in (x.error_message or "") or "Timed out" in (x.error_message or "")
            )
            timeout_penalty = timeout_count * 0.05

            # Quadratic Accuracy Efficiency Index: (PassRate^2 / 100) / (Cost + TimeoutPenalty + 0.005)
            eff_score = round(((pass_rate ** 2) / 100.0) / (total_cost + timeout_penalty + 0.005), 1)

            summaries.append(
                ModelSummary(
                    model=model,
                    cli=cli,
                    effort=effort if effort != "default" else None,
                    total_cases=total,
                    passed_cases=passed,
                    pass_rate=pass_rate,
                    avg_duration_seconds=avg_time,
                    total_input_tokens=total_in,
                    total_output_tokens=total_out,
                    total_thinking_tokens=total_think,
                    total_cost_usd=total_cost,
                    efficiency_score=eff_score,
                )
            )

        # Sort by pass rate desc, then cost asc
        summaries.sort(key=lambda s: (-s.pass_rate, s.total_cost_usd))

        md = []
        md.append("# 🏆 Personal LLM Benchmark Leaderboard")
        md.append("")
        md.append(f"> Benchmark execution completed for **{len(summaries)}** model configuration(s) across **{len(results)}** total runs.")
        md.append("")
        md.append("## 📊 Overall Model Comparison")
        md.append("")
        md.append("| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

        for s in summaries:
            effort_str = s.effort or "-"
            pass_str = f"**{s.pass_rate}%** ({s.passed_cases}/{s.total_cases})"
            cost_str = f"${s.total_cost_usd:.5f}"
            md.append(
                f"| **{s.model}** | `{s.cli}` | `{effort_str}` | {pass_str} | {s.avg_duration_seconds}s | {s.total_thinking_tokens:,} | {cost_str} | **{s.efficiency_score:,.0f}** |"
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
                c_items = [x for x in items if x.category == c]
                if not c_items:
                    row.append(" - |")
                else:
                    c_pass = sum(1 for x in c_items if x.passed)
                    c_rate = round((c_pass / len(c_items)) * 100)
                    row.append(f" {c_rate}% ({c_pass}/{len(c_items)}) |")
            md.append("".join(row))

        # Detailed Test Runs
        md.append("")
        md.append("## 📝 Detailed Test Execution Logs")
        md.append("")
        for r in results:
            status_icon = "✅ PASS" if r.passed else "❌ FAIL"
            effort_tag = f" [{r.effort}]" if r.effort else ""
            md.append(f"### {status_icon}: {r.case_title} (`{r.case_id}`)")
            md.append(f"- **Model**: `{r.model}`{effort_tag} via `{r.cli}`")
            md.append(f"- **Duration**: {r.duration_seconds:.2f}s")
            md.append(f"- **Tokens**: In: {r.token_usage.input_tokens:,} | Out: {r.token_usage.output_tokens:,} | Thinking: {r.token_usage.thinking_tokens:,} | Cost: ${r.token_usage.estimated_cost_usd:.5f}")
            if not r.passed:
                md.append(f"- **Error Details**:\n```\n{r.evaluator_logs or r.error_message or 'Test failed.'}\n```")
            md.append("")

        return "\n".join(md)
