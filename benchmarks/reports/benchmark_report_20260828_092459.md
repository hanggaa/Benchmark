# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **1** model configuration(s) across **1** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | **0.0%** (0/1) | 169.34s | 24,639 | $0.59555 | **0** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Bugfix |
| :--- | :--- | :--- | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | 0% (0/1) |

## 📝 Detailed Test Execution Logs

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 169.34s
- **Tokens**: In: 133,241 | Out: 57,171 | Thinking: 24,639 | Cost: $0.59555
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpga3ijrwc.py", line 457
    "SELECT * FROM auth WHERE token = '" OR 1=1 --'"
                                                  ^
SyntaxError: unterminated string literal (detected at line 457)
```
