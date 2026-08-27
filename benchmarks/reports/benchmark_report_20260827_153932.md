# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **2** model configuration(s) across **2** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **gpt-5.6-sol** | `codex` | `high` | **100.0%** (1/1) | 10.97s | 0 | $0.00000 | **20,000** |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | **0.0%** (0/1) | 4.87s | 0 | $0.00000 | **0** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Logic |
| :--- | :--- | :--- | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | 0% (0/1) |
| **gpt-5.6-sol** | `codex` | `high` | 100% (1/1) |

## 📝 Detailed Test Execution Logs

### ❌ FAIL: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 4.87s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"conversation_id":"","status":"ERROR","response":"","error":"invalid model selection (--model \"Gemini 3.7 Flash (High)\" --effort \"high\"): --effort is not supported for model \"Gemini 3.7 Flash (High)\"","duration_seconds":0,"num_turns":0,"usage":{"input_tokens":0,"output_tokens":0,"thinking_tokens":0,"cache_read_tokens":0,"total_tokens":0}}
```

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-sol` [high] via `codex`
- **Duration**: 10.97s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
