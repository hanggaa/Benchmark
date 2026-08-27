# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **2** model configuration(s) across **2** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **gpt-5.6-sol** | `codex` | `high` | **100.0%** (1/1) | 14.45s | 0 | $0.00000 | **20,000** |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | **100.0%** (1/1) | 8.77s | 2,456 | $0.03411 | **2,557** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Logic |
| :--- | :--- | :--- | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | 100% (1/1) |
| **gpt-5.6-sol** | `codex` | `high` | 100% (1/1) |

## 📝 Detailed Test Execution Logs

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 8.77s
- **Tokens**: In: 17,837 | Out: 2,968 | Thinking: 2,456 | Cost: $0.03411

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-sol` [high] via `codex`
- **Duration**: 14.45s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
