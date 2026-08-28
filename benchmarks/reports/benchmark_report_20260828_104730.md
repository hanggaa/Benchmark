# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **6** model configuration(s) across **84** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | **100.0%** (14/14) | 28.27s | 72,243 | $1.40702 | **71** |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | **100.0%** (14/14) | 32.81s | 141,273 | $2.18411 | **46** |
| **Gemini 3.5 Flash (High)** | `agy` | `high` | **92.9%** (13/14) | 32.24s | 150,197 | $2.13183 | **44** |
| **Gemini 3.1 Pro (High)** | `agy` | `high` | **85.7%** (12/14) | 56.45s | 46,015 | $2.25083 | **38** |
| **gpt-5.6-luna** | `codex` | `high` | **78.6%** (11/14) | 54.7s | 10,742 | $0.07827 | **944** |
| **gpt-5.6-terra** | `codex` | `high` | **78.6%** (11/14) | 31.82s | 6,870 | $0.89027 | **88** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Bugfix | Logic | Research | Tool_use |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | 100% (4/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | 100% (4/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **Gemini 3.5 Flash (High)** | `agy` | `high` | 100% (4/4) | 100% (6/6) | 50% (1/2) | 100% (2/2) |
| **Gemini 3.1 Pro (High)** | `agy` | `high` | 75% (3/4) | 100% (6/6) | 100% (2/2) | 50% (1/2) |
| **gpt-5.6-terra** | `codex` | `high` | 50% (2/4) | 100% (6/6) | 50% (1/2) | 100% (2/2) |
| **gpt-5.6-luna** | `codex` | `high` | 75% (3/4) | 83% (5/6) | 50% (1/2) | 100% (2/2) |

## 📝 Detailed Test Execution Logs

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 11.39s
- **Tokens**: In: 17,926 | Out: 4,353 | Thinking: 3,482 | Cost: $0.04283

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.33s
- **Tokens**: In: 17,839 | Out: 2,712 | Thinking: 2,202 | Cost: $0.03181

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 5.89s
- **Tokens**: In: 17,871 | Out: 1,864 | Thinking: 1,312 | Cost: $0.02531

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 21.36s
- **Tokens**: In: 18,001 | Out: 8,318 | Thinking: 6,893 | Cost: $0.07054

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 10.01s
- **Tokens**: In: 18,101 | Out: 3,690 | Thinking: 2,696 | Cost: $0.03752

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 21.70s
- **Tokens**: In: 28,562 | Out: 6,699 | Thinking: 4,234 | Cost: $0.06930

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 7.74s
- **Tokens**: In: 18,165 | Out: 3,421 | Thinking: 2,490 | Cost: $0.03579

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 7.03s
- **Tokens**: In: 20,745 | Out: 1,514 | Thinking: 779 | Cost: $0.02721

### ✅ PASS: CTF: Reverse Engineer Obfuscated Algebraic Signature Token & Keygen (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 13.83s
- **Tokens**: In: 18,115 | Out: 2,187 | Thinking: 1,610 | Cost: $0.02782

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 130.18s
- **Tokens**: In: 113,344 | Out: 45,942 | Thinking: 21,212 | Cost: $0.47213

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 13.50s
- **Tokens**: In: 17,850 | Out: 3,658 | Thinking: 1,954 | Cost: $0.03443

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.40s
- **Tokens**: In: 17,808 | Out: 2,369 | Thinking: 1,192 | Cost: $0.02671

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.10s
- **Tokens**: In: 17,873 | Out: 3,614 | Thinking: 3,083 | Cost: $0.03852

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 125.34s
- **Tokens**: In: 129,372 | Out: 35,638 | Thinking: 19,104 | Cost: $0.46710

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 20.64s
- **Tokens**: In: 37,170 | Out: 12,126 | Thinking: 9,800 | Cost: $0.11775

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 8.37s
- **Tokens**: In: 10,961 | Out: 4,000 | Thinking: 3,543 | Cost: $0.03803

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 9.97s
- **Tokens**: In: 21,609 | Out: 5,752 | Thinking: 3,781 | Cost: $0.06418

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 48.05s
- **Tokens**: In: 76,317 | Out: 25,886 | Thinking: 16,050 | Cost: $0.29472

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 16.58s
- **Tokens**: In: 23,076 | Out: 11,283 | Thinking: 9,221 | Cost: $0.09878

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 69.65s
- **Tokens**: In: 76,622 | Out: 29,006 | Thinking: 17,890 | Cost: $0.30519

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 48.16s
- **Tokens**: In: 62,070 | Out: 17,792 | Thinking: 9,342 | Cost: $0.19950

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 19.06s
- **Tokens**: In: 22,113 | Out: 5,108 | Thinking: 3,059 | Cost: $0.05943

### ✅ PASS: CTF: Reverse Engineer Obfuscated Algebraic Signature Token & Keygen (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 15.90s
- **Tokens**: In: 3,737 | Out: 2,675 | Thinking: 2,120 | Cost: $0.02372

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 98.66s
- **Tokens**: In: 99,507 | Out: 40,130 | Thinking: 25,750 | Cost: $0.43953

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 8.12s
- **Tokens**: In: 10,968 | Out: 3,908 | Thinking: 2,397 | Cost: $0.03340

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 21.80s
- **Tokens**: In: 22,215 | Out: 9,046 | Thinking: 5,349 | Cost: $0.07905

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 13.27s
- **Tokens**: In: 22,004 | Out: 7,939 | Thinking: 5,730 | Cost: $0.07693

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 61.17s
- **Tokens**: In: 68,676 | Out: 35,651 | Thinking: 27,241 | Cost: $0.35390

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 13.10s
- **Tokens**: In: 17,928 | Out: 7,487 | Thinking: 6,621 | Cost: $0.06635

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 9.76s
- **Tokens**: In: 17,842 | Out: 4,977 | Thinking: 4,573 | Cost: $0.04919

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 10.24s
- **Tokens**: In: 17,881 | Out: 5,593 | Thinking: 5,149 | Cost: $0.05369

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 73.78s
- **Tokens**: In: 146,992 | Out: 30,266 | Thinking: 20,497 | Cost: $0.38234

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 16.58s
- **Tokens**: In: 18,100 | Out: 9,499 | Thinking: 8,530 | Cost: $0.08118

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 9.24s
- **Tokens**: In: 9,829 | Out: 5,683 | Thinking: 4,982 | Cost: $0.04889

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 26.40s
- **Tokens**: In: 18,167 | Out: 14,789 | Thinking: 14,053 | Cost: $0.12178

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 41.93s
- **Tokens**: In: 79,450 | Out: 10,701 | Thinking: 6,415 | Cost: $0.17944

### ✅ PASS: CTF: Reverse Engineer Obfuscated Algebraic Signature Token & Keygen (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 7.42s
- **Tokens**: In: 18,120 | Out: 3,047 | Thinking: 2,440 | Cost: $0.03417

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 74.75s
- **Tokens**: In: 9,897 | Out: 38,592 | Thinking: 36,117 | Cost: $0.28911

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 9.10s
- **Tokens**: In: 17,859 | Out: 4,385 | Thinking: 3,303 | Cost: $0.04222

### ❌ FAIL: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 52.67s
- **Tokens**: In: 66,531 | Out: 12,451 | Thinking: 9,255 | Cost: $0.15039
- **Error Details**:
```
Missing required heading: 'Recommendation Matrix'
Missing required content/keyword: '| Engine |'
Missing required content/keyword: '$'
```

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 10.35s
- **Tokens**: In: 17,878 | Out: 5,433 | Thinking: 4,870 | Cost: $0.05205

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 96.04s
- **Tokens**: In: 250,868 | Out: 38,202 | Thinking: 23,392 | Cost: $0.58102

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 45.32s
- **Tokens**: In: 18,201 | Out: 5,250 | Thinking: 4,589 | Cost: $0.19309

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 22.29s
- **Tokens**: In: 10,000 | Out: 2,467 | Thinking: 2,129 | Cost: $0.09901

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 38.69s
- **Tokens**: In: 10,027 | Out: 4,504 | Thinking: 3,988 | Cost: $0.15752

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 82.24s
- **Tokens**: In: 10,159 | Out: 9,844 | Thinking: 8,683 | Cost: $0.30838

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 45.54s
- **Tokens**: In: 10,256 | Out: 5,180 | Thinking: 4,571 | Cost: $0.17698

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 36.07s
- **Tokens**: In: 10,130 | Out: 3,937 | Thinking: 3,310 | Cost: $0.13910

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 32.55s
- **Tokens**: In: 10,319 | Out: 3,815 | Thinking: 3,179 | Cost: $0.13578

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 21.07s
- **Tokens**: In: 13,385 | Out: 1,466 | Thinking: 749 | Cost: $0.08191

### ❌ FAIL: CTF: Reverse Engineer Obfuscated Algebraic Signature Token & Keygen (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 12.13s
- **Tokens**: In: 18,387 | Out: 816 | Thinking: 789 | Cost: $0.07004
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpfoeoebx2.py", line 2
    Sorry, I cannot fulfill your request. I am unable to write key generators or provide code designed to bypass software licensing and authentication mechanisms.
             ^^^^^^
SyntaxError: invalid syntax
```

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 154.57s
- **Tokens**: In: 43,120 | Out: 13,079 | Thinking: 4,726 | Cost: $0.48912

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 25.45s
- **Tokens**: In: 10,008 | Out: 1,724 | Thinking: 898 | Cost: $0.06942

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 31.66s
- **Tokens**: In: 9,962 | Out: 1,820 | Thinking: 1,012 | Cost: $0.07246

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 62.66s
- **Tokens**: In: 10,028 | Out: 7,801 | Thinking: 7,392 | Cost: $0.25804

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
- **Duration**: 15.15s
- **Tokens**: In: 21,086 | Out: 581 | Thinking: 0 | Cost: $0.05114

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 11.03s
- **Tokens**: In: 21,000 | Out: 393 | Thinking: 137 | Cost: $0.04836

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 17.41s
- **Tokens**: In: 21,027 | Out: 666 | Thinking: 310 | Cost: $0.05576

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 30.41s
- **Tokens**: In: 21,146 | Out: 1,347 | Thinking: 516 | Cost: $0.06664

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 18.02s
- **Tokens**: In: 21,245 | Out: 735 | Thinking: 212 | Cost: $0.05790

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 21.72s
- **Tokens**: In: 21,124 | Out: 920 | Thinking: 516 | Cost: $0.06148

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 21.88s
- **Tokens**: In: 21,263 | Out: 965 | Thinking: 516 | Cost: $0.06230

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 16.37s
- **Tokens**: In: 21,150 | Out: 655 | Thinking: 495 | Cost: $0.06014

### ❌ FAIL: CTF: Reverse Engineer Obfuscated Algebraic Signature Token & Keygen (`sec_ctf_01_keygen`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 7.15s
- **Tokens**: In: 21,249 | Out: 128 | Thinking: 108 | Cost: $0.04938
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmp3fdfef51.py", line 2
    I can’t help generate tokens that bypass an authentication/license verification routine.
         ^
SyntaxError: invalid character '’' (U+2019)
```

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 66.80s
- **Tokens**: In: 21,184 | Out: 3,491 | Thinking: 2,437 | Cost: $0.11550
- **Error Details**:
```
Test failure (exit code 1):
Traceback (most recent call last):
  File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpghf57dsa.py", line 172, in <module>
    assert is_safe is True, f"Legitimate query was wrongly blocked: {legit} (Reason: {reason})"
           ^^^^^^^^^^^^^^^
AssertionError: Legitimate query was wrongly blocked: SELECT data->>'user_id' AS uid, metadata#>>'{geo,country}' FROM telemetry_events WHERE timestamp > '2026-01-01' (Reason: INLINE_COMMENT)
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 43.67s
- **Tokens**: In: 44,547 | Out: 2,100 | Thinking: 73 | Cost: $0.12121

### ❌ FAIL: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 120.01s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
Timed out after 120s
```

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 25.19s
- **Tokens**: In: 21,035 | Out: 996 | Thinking: 516 | Cost: $0.06426

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 30.74s
- **Tokens**: In: 21,129 | Out: 1,457 | Thinking: 1,034 | Cost: $0.07619

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 34.58s
- **Tokens**: In: 19,528 | Out: 1,710 | Thinking: 1,034 | Cost: $0.00738

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 8.31s
- **Tokens**: In: 19,442 | Out: 237 | Thinking: 80 | Cost: $0.00445

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 12.99s
- **Tokens**: In: 19,469 | Out: 515 | Thinking: 117 | Cost: $0.00483

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
- **Duration**: 24.46s
- **Tokens**: In: 19,687 | Out: 1,131 | Thinking: 516 | Cost: $0.00609

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 45.16s
- **Tokens**: In: 19,566 | Out: 2,118 | Thinking: 1,552 | Cost: $0.00868

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 23.96s
- **Tokens**: In: 19,705 | Out: 1,016 | Thinking: 516 | Cost: $0.00614

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 43.37s
- **Tokens**: In: 19,592 | Out: 2,208 | Thinking: 2,070 | Cost: $0.00942

### ✅ PASS: CTF: Reverse Engineer Obfuscated Algebraic Signature Token & Keygen (`sec_ctf_01_keygen`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 15.40s
- **Tokens**: In: 19,691 | Out: 623 | Thinking: 150 | Cost: $0.00505

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 180.01s
- **Tokens**: In: 0 | Out: 0 | Thinking: 0 | Cost: $0.00000
- **Error Details**:
```
Timed out after 180s
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 28.64s
- **Tokens**: In: 19,457 | Out: 1,198 | Thinking: 65 | Cost: $0.00559

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
- **Duration**: 50.71s
- **Tokens**: In: 19,477 | Out: 2,596 | Thinking: 1,949 | Cost: $0.00953

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 58.17s
- **Tokens**: In: 19,571 | Out: 3,011 | Thinking: 2,693 | Cost: $0.01112
