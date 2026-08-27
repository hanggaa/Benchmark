# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **1** model configuration(s) across **1** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **gemini-2.5-flash** | `agy` | `-` | **0.0%** (0/1) | 4.62s | 0 | $0.00000 | **0** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Logic |
| :--- | :--- | :--- | :---: |
| **gemini-2.5-flash** | `agy` | `default` | 0% (0/1) |

## 📝 Detailed Test Execution Logs

### ❌ FAIL: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gemini-2.5-flash` via `agy`
- **Duration**: 4.62s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"conversation_id":"","status":"ERROR","response":"","error":"invalid model selection (--model \"gemini-2.5-flash\" --effort \"\"): model gemini-2.5-flash is not recognized as a known model or custom model in settings\nAvailable models:\n  Gemini 3.7 Flash (High)\n  Gemini 3.7 Flash (Medium)\n  Gemini 3.7 Flash (Low)\n  Gemini 3.6 Flash (High)\n  Gemini 3.6 Flash (Medium)\n  Gemini 3.6 Flash (Low)\n  Gemini 3.5 Flash (High)\n  Gemini 3.5 Flash (Medium)\n  Gemini 3.5 Flash (Low)\n  Gemini 3.1 Pro (High)\n  Gemini 3.1 Pro (Low)\n  Claude Sonnet 4.6 (Thinking)\n  Claude Opus 4.6 (Thinking)\n  GPT-OSS 120B (Medium)","duration_seconds":0,"num_turns":0,"usage":{"input_tokens":0,"output_tokens":0,"thinking_tokens":0,"cache_read_tokens":0,"total_tokens":0}}
```
