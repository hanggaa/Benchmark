# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **6** model configuration(s) across **84** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | **92.9%** (13/14) | 27.49s | 79,882 | $1.47483 | **63** |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | **92.9%** (13/14) | 30.04s | 125,292 | $2.08590 | **44** |
| **Gemini 3.5 Flash (High)** | `agy` | `high` | **92.9%** (13/14) | 42.67s | 182,129 | $3.04435 | **30** |
| **gpt-5.6-terra** | `codex` | `high` | **85.7%** (12/14) | 34.57s | 11,643 | $1.43492 | **60** |
| **Gemini 3.1 Pro (High)** | `agy` | `high` | **85.7%** (12/14) | 50.3s | 54,271 | $2.18163 | **39** |
| **gpt-5.6-luna** | `codex` | `high` | **78.6%** (11/14) | 48.7s | 14,027 | $0.09200 | **810** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Bugfix | Logic | Research | Tool_use |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | 75% (3/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | 75% (3/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **Gemini 3.5 Flash (High)** | `agy` | `high` | 75% (3/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **Gemini 3.1 Pro (High)** | `agy` | `high` | 75% (3/4) | 100% (6/6) | 100% (2/2) | 50% (1/2) |
| **gpt-5.6-terra** | `codex` | `high` | 50% (2/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **gpt-5.6-luna** | `codex` | `high` | 75% (3/4) | 83% (5/6) | 50% (1/2) | 100% (2/2) |

## 📝 Detailed Test Execution Logs

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.70s
- **Tokens**: In: 17,928 | Out: 3,652 | Thinking: 2,745 | Cost: $0.03744

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 10.46s
- **Tokens**: In: 17,844 | Out: 3,945 | Thinking: 3,507 | Cost: $0.04133

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 6.67s
- **Tokens**: In: 17,878 | Out: 2,583 | Thinking: 2,076 | Cost: $0.03088

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 16.08s
- **Tokens**: In: 17,997 | Out: 7,157 | Thinking: 5,868 | Cost: $0.06234

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 12.07s
- **Tokens**: In: 18,101 | Out: 4,505 | Thinking: 3,670 | Cost: $0.04423

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 28.69s
- **Tokens**: In: 49,075 | Out: 10,993 | Thinking: 7,049 | Cost: $0.11287

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 6.78s
- **Tokens**: In: 18,168 | Out: 2,430 | Thinking: 1,687 | Cost: $0.02907

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 7.16s
- **Tokens**: In: 21,451 | Out: 2,251 | Thinking: 1,310 | Cost: $0.03250

### ✅ PASS: CTF: Reverse Engineer Obfuscated License Key Validator & Keygen (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 4.40s
- **Tokens**: In: 18,121 | Out: 1,991 | Thinking: 1,419 | Cost: $0.02638

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 140.54s
- **Tokens**: In: 117,023 | Out: 50,464 | Thinking: 22,336 | Cost: $0.51525
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmp9wzjv847.py", line 459
    "SELECT * FROM auth WHERE token = '" OR ""="'"
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 12.27s
- **Tokens**: In: 17,851 | Out: 3,307 | Thinking: 1,643 | Cost: $0.03195

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 12.26s
- **Tokens**: In: 17,807 | Out: 3,228 | Thinking: 1,459 | Cost: $0.03093

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 5.69s
- **Tokens**: In: 17,872 | Out: 2,262 | Thinking: 1,724 | Cost: $0.02835

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 112.12s
- **Tokens**: In: 150,801 | Out: 35,027 | Thinking: 23,389 | Cost: $0.45132

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 29.16s
- **Tokens**: In: 45,388 | Out: 17,289 | Thinking: 12,032 | Cost: $0.16388

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 7.33s
- **Tokens**: In: 17,357 | Out: 4,390 | Thinking: 3,485 | Cost: $0.04713

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 11.53s
- **Tokens**: In: 23,070 | Out: 6,371 | Thinking: 4,232 | Cost: $0.06928

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 47.16s
- **Tokens**: In: 68,895 | Out: 24,491 | Thinking: 12,790 | Cost: $0.25185

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 23.96s
- **Tokens**: In: 33,512 | Out: 16,298 | Thinking: 13,920 | Cost: $0.14840

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 29.10s
- **Tokens**: In: 37,385 | Out: 13,317 | Thinking: 7,656 | Cost: $0.13343

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 19.44s
- **Tokens**: In: 26,272 | Out: 10,362 | Thinking: 7,638 | Cost: $0.09638

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 18.37s
- **Tokens**: In: 26,182 | Out: 3,439 | Thinking: 2,147 | Cost: $0.05127

### ✅ PASS: CTF: Reverse Engineer Obfuscated License Key Validator & Keygen (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 4.55s
- **Tokens**: In: 16,710 | Out: 3,347 | Thinking: 2,070 | Cost: $0.03743

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 125.57s
- **Tokens**: In: 120,220 | Out: 43,297 | Thinking: 21,677 | Cost: $0.50421
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpf1pbzdwd.py", line 202
    "SELECT * FROM auth WHERE token = '" OR ""="'"
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 5.19s
- **Tokens**: In: 10,974 | Out: 2,282 | Thinking: 1,232 | Cost: $0.02294

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 18.24s
- **Tokens**: In: 19,099 | Out: 4,092 | Thinking: 2,269 | Cost: $0.04658

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 12.81s
- **Tokens**: In: 10,990 | Out: 8,190 | Thinking: 7,695 | Cost: $0.06934

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 68.19s
- **Tokens**: In: 96,967 | Out: 38,265 | Thinking: 26,449 | Cost: $0.44377

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 30.71s
- **Tokens**: In: 69,845 | Out: 11,496 | Thinking: 7,506 | Cost: $0.14351

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 11.45s
- **Tokens**: In: 17,841 | Out: 6,289 | Thinking: 5,812 | Cost: $0.05876

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 6.08s
- **Tokens**: In: 17,875 | Out: 3,427 | Thinking: 2,935 | Cost: $0.03726

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 69.31s
- **Tokens**: In: 85,369 | Out: 29,225 | Thinking: 20,669 | Cost: $0.34215

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 19.36s
- **Tokens**: In: 51,441 | Out: 12,527 | Thinking: 7,805 | Cost: $0.12400

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 39.56s
- **Tokens**: In: 45,834 | Out: 20,305 | Thinking: 15,158 | Cost: $0.19945

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 25.60s
- **Tokens**: In: 70,860 | Out: 11,878 | Thinking: 8,758 | Cost: $0.14047

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 44.66s
- **Tokens**: In: 136,405 | Out: 8,270 | Thinking: 3,952 | Cost: $0.18853

### ✅ PASS: CTF: Reverse Engineer Obfuscated License Key Validator & Keygen (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 4.45s
- **Tokens**: In: 18,116 | Out: 2,575 | Thinking: 2,018 | Cost: $0.03081

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 101.67s
- **Tokens**: In: 98,126 | Out: 50,139 | Thinking: 40,394 | Cost: $0.50119
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpknx_9msb.py", line 298
    "SELECT * FROM auth WHERE token = '" OR ""="'"
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 11.19s
- **Tokens**: In: 32,749 | Out: 6,301 | Thinking: 3,736 | Cost: $0.06373

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 62.01s
- **Tokens**: In: 67,470 | Out: 10,484 | Thinking: 8,384 | Cost: $0.14656

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 23.23s
- **Tokens**: In: 17,868 | Out: 11,887 | Thinking: 11,184 | Cost: $0.09992

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 148.13s
- **Tokens**: In: 226,297 | Out: 73,521 | Thinking: 43,818 | Cost: $0.96802

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 26.86s
- **Tokens**: In: 18,201 | Out: 3,320 | Thinking: 2,667 | Cost: $0.13531

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 20.96s
- **Tokens**: In: 10,002 | Out: 2,431 | Thinking: 2,095 | Cost: $0.09797

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 34.01s
- **Tokens**: In: 10,031 | Out: 4,169 | Thinking: 3,602 | Cost: $0.14671

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 42.53s
- **Tokens**: In: 10,153 | Out: 5,566 | Thinking: 4,602 | Cost: $0.18297

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 38.63s
- **Tokens**: In: 10,256 | Out: 4,340 | Thinking: 3,566 | Cost: $0.14930

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 52.17s
- **Tokens**: In: 10,132 | Out: 6,112 | Thinking: 5,486 | Cost: $0.20437

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 31.92s
- **Tokens**: In: 10,323 | Out: 3,931 | Thinking: 3,250 | Cost: $0.13859

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 15.58s
- **Tokens**: In: 10,168 | Out: 1,509 | Thinking: 1,167 | Cost: $0.07063

### ✅ PASS: CTF: Reverse Engineer Obfuscated License Key Validator & Keygen (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 23.17s
- **Tokens**: In: 10,269 | Out: 3,110 | Thinking: 2,519 | Cost: $0.11518

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 166.83s
- **Tokens**: In: 10,198 | Out: 20,769 | Thinking: 19,902 | Cost: $0.64063
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmp5x1dcerg.py", line 73
    "SELECT * FROM auth WHERE token = '" OR ""="'"
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 18.62s
- **Tokens**: In: 18,117 | Out: 1,747 | Thinking: 1,090 | Cost: $0.08785

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 27.04s
- **Tokens**: In: 9,967 | Out: 2,563 | Thinking: 1,450 | Cost: $0.09018

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 25.82s
- **Tokens**: In: 10,026 | Out: 3,244 | Thinking: 2,875 | Cost: $0.12192

### ❌ FAIL: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 180.02s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
Timed out after 180s
```

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 15.37s
- **Tokens**: In: 21,086 | Out: 579 | Thinking: 0 | Cost: $0.05112

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 8.58s
- **Tokens**: In: 21,000 | Out: 233 | Thinking: 47 | Cost: $0.04736

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 26.49s
- **Tokens**: In: 21,027 | Out: 1,201 | Thinking: 707 | Cost: $0.06695

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 111.67s
- **Tokens**: In: 21,146 | Out: 5,149 | Thinking: 3,878 | Cost: $0.15261

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 21.19s
- **Tokens**: In: 21,245 | Out: 845 | Thinking: 377 | Cost: $0.06120

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 19.08s
- **Tokens**: In: 21,124 | Out: 803 | Thinking: 420 | Cost: $0.06097

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 13.11s
- **Tokens**: In: 21,263 | Out: 422 | Thinking: 0 | Cost: $0.05164

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 24.02s
- **Tokens**: In: 21,150 | Out: 931 | Thinking: 516 | Cost: $0.06166

### ❌ FAIL: CTF: Reverse Engineer Obfuscated License Key Validator & Keygen (`sec_ctf_01_keygen`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 7.34s
- **Tokens**: In: 21,247 | Out: 73 | Thinking: 55 | Cost: $0.04603
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpz3qgu0up.py", line 2
    I can’t help generate keys that bypass proprietary license verification.
         ^
SyntaxError: invalid character '’' (U+2019)
```

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 59.60s
- **Tokens**: In: 21,184 | Out: 3,038 | Thinking: 1,891 | Cost: $0.10556
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmp4kwmpqz3.py", line 174
    "SELECT * FROM auth WHERE token = '" OR ""="'"
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 35.52s
- **Tokens**: In: 44,542 | Out: 1,327 | Thinking: 100 | Cost: $0.11430

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 101.82s
- **Tokens**: In: 187,811 | Out: 4,434 | Thinking: 2,749 | Cost: $0.49187

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 19.78s
- **Tokens**: In: 21,035 | Out: 838 | Thinking: 387 | Cost: $0.06061

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 20.43s
- **Tokens**: In: 21,129 | Out: 880 | Thinking: 516 | Cost: $0.06305

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 21.61s
- **Tokens**: In: 19,528 | Out: 976 | Thinking: 410 | Cost: $0.00575

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 11.86s
- **Tokens**: In: 19,442 | Out: 358 | Thinking: 72 | Cost: $0.00458

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 26.22s
- **Tokens**: In: 19,469 | Out: 1,185 | Thinking: 727 | Cost: $0.00637

### ❌ FAIL: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 120.01s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
Timed out after 120s
```

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 24.39s
- **Tokens**: In: 19,687 | Out: 1,146 | Thinking: 516 | Cost: $0.00611

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 21.46s
- **Tokens**: In: 19,566 | Out: 991 | Thinking: 516 | Cost: $0.00590

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 22.37s
- **Tokens**: In: 19,705 | Out: 984 | Thinking: 516 | Cost: $0.00592

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 47.80s
- **Tokens**: In: 19,592 | Out: 2,461 | Thinking: 2,070 | Cost: $0.00954

### ✅ PASS: CTF: Reverse Engineer Obfuscated License Key Validator & Keygen (`sec_ctf_01_keygen`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 13.63s
- **Tokens**: In: 19,689 | Out: 538 | Thinking: 89 | Cost: $0.00487

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 152.47s
- **Tokens**: In: 19,626 | Out: 8,279 | Thinking: 7,009 | Cost: $0.02245
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpw7mit4al.py", line 184
    "SELECT * FROM auth WHERE token = '" OR ""="'"
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 36.63s
- **Tokens**: In: 19,457 | Out: 1,766 | Thinking: 34 | Cost: $0.00623

### ❌ FAIL: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 120.01s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
Timed out after 120s
```

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 34.12s
- **Tokens**: In: 19,477 | Out: 1,640 | Thinking: 1,034 | Cost: $0.00728

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 29.15s
- **Tokens**: In: 19,571 | Out: 1,391 | Thinking: 1,034 | Cost: $0.00700
