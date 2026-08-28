# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **1** model configuration(s) across **5** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | **60.0%** (3/5) | 53.97s | 8,804 | $0.11527 | **499** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Bugfix | Logic | Tool_use |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | 50% (1/2) | 100% (2/2) | 0% (0/1) |

## 📝 Detailed Test Execution Logs

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 11.68s
- **Tokens**: In: 18,099 | Out: 4,321 | Thinking: 3,324 | Cost: $0.04224

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 13.11s
- **Tokens**: In: 17,973 | Out: 5,104 | Thinking: 4,369 | Cost: $0.04900

### ✅ PASS: CTF: Reverse Engineer Obfuscated License Key Validator & Keygen (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 5.07s
- **Tokens**: In: 18,120 | Out: 1,672 | Thinking: 1,111 | Cost: $0.02403

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 120.01s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
Timed out after 120s
```

### ❌ FAIL: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 120.01s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
Timed out after 120s
```
