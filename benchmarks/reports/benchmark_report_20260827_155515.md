# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **4** model configuration(s) across **36** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **gpt-5.6-terra** | `codex` | `high` | **100.0%** (9/9) | 38.14s | 0 | $0.00000 | **20,000** |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | **100.0%** (9/9) | 11.0s | 18,677 | $0.30539 | **322** |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | **100.0%** (9/9) | 19.58s | 62,520 | $0.90314 | **110** |
| **opencode/deepseek-v4-
  flash-free** | `opencode` | `-` | **0.0%** (0/9) | 0.88s | 0 | $0.00000 | **0** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Bugfix | Logic | Research | Tool_use |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | 100% (2/2) | 100% (4/4) | 100% (2/2) | 100% (1/1) |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | 100% (2/2) | 100% (4/4) | 100% (2/2) | 100% (1/1) |
| **gpt-5.6-terra** | `codex` | `high` | 100% (2/2) | 100% (4/4) | 100% (2/2) | 100% (1/1) |
| **opencode/deepseek-v4-
  flash-free** | `opencode` | `default` | 0% (0/2) | 0% (0/4) | 0% (0/2) | 0% (0/1) |

## 📝 Detailed Test Execution Logs

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 12.45s
- **Tokens**: In: 17,933 | Out: 3,999 | Thinking: 3,171 | Cost: $0.03944

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 7.49s
- **Tokens**: In: 17,844 | Out: 2,244 | Thinking: 1,778 | Cost: $0.02991

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 6.74s
- **Tokens**: In: 17,880 | Out: 2,329 | Thinking: 1,892 | Cost: $0.03054

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 22.87s
- **Tokens**: In: 17,996 | Out: 5,183 | Thinking: 3,729 | Cost: $0.04473

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 8.38s
- **Tokens**: In: 18,167 | Out: 2,880 | Thinking: 2,155 | Cost: $0.03327

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 10.01s
- **Tokens**: In: 21,387 | Out: 2,179 | Thinking: 1,444 | Cost: $0.03633

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 12.91s
- **Tokens**: In: 17,855 | Out: 3,177 | Thinking: 1,548 | Cost: $0.03203

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 10.61s
- **Tokens**: In: 17,809 | Out: 2,633 | Thinking: 1,441 | Cost: $0.03003

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 7.55s
- **Tokens**: In: 17,877 | Out: 2,221 | Thinking: 1,519 | Cost: $0.02910

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 15.66s
- **Tokens**: In: 19,197 | Out: 9,579 | Thinking: 8,756 | Cost: $0.07420

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 6.39s
- **Tokens**: In: 10,963 | Out: 3,880 | Thinking: 3,416 | Cost: $0.03489

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 14.17s
- **Tokens**: In: 29,038 | Out: 9,030 | Thinking: 6,409 | Cost: $0.09268

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 60.61s
- **Tokens**: In: 98,834 | Out: 25,239 | Thinking: 13,016 | Cost: $0.37957

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 16.65s
- **Tokens**: In: 26,362 | Out: 10,282 | Thinking: 7,928 | Cost: $0.09220

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 14.24s
- **Tokens**: In: 17,752 | Out: 3,967 | Thinking: 2,601 | Cost: $0.04866

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 9.15s
- **Tokens**: In: 10,971 | Out: 3,632 | Thinking: 2,258 | Cost: $0.03068

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 16.71s
- **Tokens**: In: 15,732 | Out: 6,261 | Thinking: 4,582 | Cost: $0.05437

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 22.62s
- **Tokens**: In: 10,992 | Out: 14,067 | Thinking: 13,554 | Cost: $0.09589

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 19.45s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 9.95s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 14.48s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 92.48s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 12.02s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 18.13s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 43.41s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 109.60s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 23.75s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000

### ❌ FAIL: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `opencode/deepseek-v4-
  flash-free` via `opencode`
- **Duration**: 1.18s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"type":"error","timestamp":1787820908322,"sessionID":"ses_fbd91e1d8ffe03DOiifyRkDFbP","error":{"name":"UnknownError","data":{"message":"Unexpected server error. Check server logs for details.","ref":"err_acfc605e"}}}
```

### ❌ FAIL: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `opencode/deepseek-v4-
  flash-free` via `opencode`
- **Duration**: 0.82s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"type":"error","timestamp":1787820909148,"sessionID":"ses_fbd91de7effeg8emauBEuff5C3","error":{"name":"UnknownError","data":{"message":"Unexpected server error. Check server logs for details.","ref":"err_ff7f5a72"}}}
```

### ❌ FAIL: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `opencode/deepseek-v4-
  flash-free` via `opencode`
- **Duration**: 0.84s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"type":"error","timestamp":1787820909990,"sessionID":"ses_fbd91db4bffevzYtM2CpOh7wHr","error":{"name":"UnknownError","data":{"message":"Unexpected server error. Check server logs for details.","ref":"err_524e047b"}}}
```

### ❌ FAIL: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `opencode/deepseek-v4-
  flash-free` via `opencode`
- **Duration**: 0.85s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"type":"error","timestamp":1787820910839,"sessionID":"ses_fbd91d7f9ffeP4fgL3U8XpUb0M","error":{"name":"UnknownError","data":{"message":"Unexpected server error. Check server logs for details.","ref":"err_be53318b"}}}
```

### ❌ FAIL: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `opencode/deepseek-v4-
  flash-free` via `opencode`
- **Duration**: 0.85s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"type":"error","timestamp":1787820911690,"sessionID":"ses_fbd91d4a7ffeF77jUawLaGXtIv","error":{"name":"UnknownError","data":{"message":"Unexpected server error. Check server logs for details.","ref":"err_1f143574"}}}
```

### ❌ FAIL: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `opencode/deepseek-v4-
  flash-free` via `opencode`
- **Duration**: 0.84s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"type":"error","timestamp":1787820912536,"sessionID":"ses_fbd91d155ffetertFJgdWpNnC8","error":{"name":"UnknownError","data":{"message":"Unexpected server error. Check server logs for details.","ref":"err_544e0d34"}}}
```

### ❌ FAIL: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `opencode/deepseek-v4-
  flash-free` via `opencode`
- **Duration**: 0.84s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"type":"error","timestamp":1787820913379,"sessionID":"ses_fbd91ce09ffejs40vImro7Xy74","error":{"name":"UnknownError","data":{"message":"Unexpected server error. Check server logs for details.","ref":"err_85995aeb"}}}
```

### ❌ FAIL: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `opencode/deepseek-v4-
  flash-free` via `opencode`
- **Duration**: 0.85s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"type":"error","timestamp":1787820914224,"sessionID":"ses_fbd91cac0ffepW9PKckHAMz4rq","error":{"name":"UnknownError","data":{"message":"Unexpected server error. Check server logs for details.","ref":"err_9f8ba325"}}}
```

### ❌ FAIL: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `opencode/deepseek-v4-
  flash-free` via `opencode`
- **Duration**: 0.84s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
{"type":"error","timestamp":1787820915067,"sessionID":"ses_fbd91c770ffe8X2ArN76CiXBgl","error":{"name":"UnknownError","data":{"message":"Unexpected server error. Check server logs for details.","ref":"err_9c95dce4"}}}
```
