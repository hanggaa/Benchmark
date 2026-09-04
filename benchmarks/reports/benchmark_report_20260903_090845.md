# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **6** model configuration(s) across **84** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | **100.0%** (14/14) | 29.14s | 61,668 | $1.27701 | **78** |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | **100.0%** (14/14) | 29.35s | 132,789 | $1.96298 | **51** |
| **Gemini 3.1 Pro (High)** | `agy` | `high` | **92.9%** (13/14) | 60.89s | 86,424 | $3.71330 | **23** |
| **Gemini 3.8 Flash (High)** | `agy` | `high` | **92.9%** (13/14) | 88.74s | 232,992 | $4.06898 | **21** |
| **gpt-5.6-terra** | `codex` | `high` | **85.7%** (12/14) | 32.36s | 9,752 | $1.74236 | **42** |
| **gpt-5.6-luna** | `codex` | `high` | **78.6%** (11/14) | 78.01s | 39,053 | $0.54608 | **112** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Bugfix | Logic | Research | Tool_use |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Gemini 3.8 Flash (High)** | `agy` | `high` | 75% (3/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | 100% (4/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | 100% (4/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **Gemini 3.1 Pro (High)** | `agy` | `high` | 75% (3/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **gpt-5.6-terra** | `codex` | `high` | 75% (3/4) | 83% (5/6) | 100% (2/2) | 100% (2/2) |
| **gpt-5.6-luna** | `codex` | `high` | 75% (3/4) | 83% (5/6) | 100% (2/2) | 50% (1/2) |

## 📝 Detailed Test Execution Logs

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 139.23s
- **Tokens**: In: 99,415 | Out: 29,811 | Thinking: 25,365 | Cost: $0.38014

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 23.76s
- **Tokens**: In: 17,868 | Out: 7,697 | Thinking: 7,211 | Cost: $0.06931

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 71.72s
- **Tokens**: In: 43,170 | Out: 21,906 | Thinking: 19,299 | Cost: $0.20067

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 121.61s
- **Tokens**: In: 101,265 | Out: 33,362 | Thinking: 24,308 | Cost: $0.40917

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 18.89s
- **Tokens**: In: 18,135 | Out: 6,640 | Thinking: 5,620 | Cost: $0.05958

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 155.04s
- **Tokens**: In: 120,889 | Out: 38,933 | Thinking: 27,495 | Cost: $0.49706

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 19.19s
- **Tokens**: In: 25,758 | Out: 5,450 | Thinking: 3,480 | Cost: $0.05968

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 23.07s
- **Tokens**: In: 34,191 | Out: 3,767 | Thinking: 2,258 | Cost: $0.06045

### ❌ FAIL: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 13.42s
- **Tokens**: In: 18,178 | Out: 0 | Thinking: 0 | Cost: $0.01363
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmp7ei7t20m.py", line 2
    This request was blocked by Gemini's filters. They can occasionally trigger by mistake on safe coding, security, or biology-related queries. Please try rephrasing your prompt. You can [send feedback](https://ai.google.dev/gemini-api/docs/troubleshooting#file-bug) or read more about [our policies here](https://policies.google.com/terms/generative-ai/use-policy).
                                      ^
SyntaxError: unterminated string literal (detected at line 2)
```

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 290.85s
- **Tokens**: In: 230,705 | Out: 75,470 | Thinking: 45,779 | Cost: $1.19386

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 14.09s
- **Tokens**: In: 17,885 | Out: 3,192 | Thinking: 1,725 | Cost: $0.03185

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 21.86s
- **Tokens**: In: 17,837 | Out: 5,145 | Thinking: 1,966 | Cost: $0.04004

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 47.16s
- **Tokens**: In: 17,901 | Out: 16,704 | Thinking: 16,107 | Cost: $0.13647

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.8 Flash (High)` [high] via `agy`
- **Duration**: 282.46s
- **Tokens**: In: 212,867 | Out: 64,485 | Thinking: 52,379 | Cost: $0.91708

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 11.49s
- **Tokens**: In: 17,960 | Out: 4,405 | Thinking: 3,503 | Cost: $0.04312

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.84s
- **Tokens**: In: 17,867 | Out: 2,891 | Thinking: 2,466 | Cost: $0.03349

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 6.71s
- **Tokens**: In: 17,912 | Out: 2,325 | Thinking: 1,776 | Cost: $0.02881

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 14.81s
- **Tokens**: In: 18,035 | Out: 4,742 | Thinking: 3,293 | Cost: $0.04366

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 11.43s
- **Tokens**: In: 18,135 | Out: 4,172 | Thinking: 3,232 | Cost: $0.04137

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.57s
- **Tokens**: In: 18,008 | Out: 3,046 | Thinking: 2,234 | Cost: $0.03331

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 8.43s
- **Tokens**: In: 18,202 | Out: 2,527 | Thinking: 1,853 | Cost: $0.03008

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 11.72s
- **Tokens**: In: 21,103 | Out: 1,825 | Thinking: 1,028 | Cost: $0.02958

### ✅ PASS: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 12.59s
- **Tokens**: In: 18,173 | Out: 2,240 | Thinking: 1,648 | Cost: $0.02821

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 187.68s
- **Tokens**: In: 128,727 | Out: 55,393 | Thinking: 19,599 | Cost: $0.56883

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 10.56s
- **Tokens**: In: 17,887 | Out: 2,578 | Thinking: 1,105 | Cost: $0.02723

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 10.43s
- **Tokens**: In: 17,841 | Out: 2,857 | Thinking: 1,751 | Cost: $0.03066

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 8.35s
- **Tokens**: In: 17,904 | Out: 2,612 | Thinking: 1,781 | Cost: $0.02990

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 94.38s
- **Tokens**: In: 85,849 | Out: 24,746 | Thinking: 16,399 | Cost: $0.30876

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 17.61s
- **Tokens**: In: 19,230 | Out: 10,843 | Thinking: 9,999 | Cost: $0.09258

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 9.02s
- **Tokens**: In: 18,080 | Out: 4,703 | Thinking: 3,771 | Cost: $0.04992

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 6.76s
- **Tokens**: In: 11,028 | Out: 3,890 | Thinking: 3,361 | Cost: $0.03699

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 52.02s
- **Tokens**: In: 66,701 | Out: 27,117 | Thinking: 13,664 | Cost: $0.27100

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 15.49s
- **Tokens**: In: 22,125 | Out: 9,603 | Thinking: 8,052 | Cost: $0.08739

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 38.18s
- **Tokens**: In: 41,574 | Out: 21,947 | Thinking: 14,306 | Cost: $0.19467

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 10.09s
- **Tokens**: In: 11,320 | Out: 6,757 | Thinking: 6,089 | Cost: $0.05819

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 17.55s
- **Tokens**: In: 25,285 | Out: 5,603 | Thinking: 4,170 | Cost: $0.06707

### ✅ PASS: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 24.84s
- **Tokens**: In: 15,988 | Out: 3,862 | Thinking: 2,628 | Cost: $0.04080

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 113.62s
- **Tokens**: In: 96,568 | Out: 46,293 | Thinking: 27,623 | Cost: $0.49113

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 5.93s
- **Tokens**: In: 11,003 | Out: 2,824 | Thinking: 1,759 | Cost: $0.02697

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 18.87s
- **Tokens**: In: 16,539 | Out: 5,726 | Thinking: 3,734 | Cost: $0.05246

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 17.63s
- **Tokens**: In: 28,834 | Out: 9,694 | Thinking: 8,129 | Cost: $0.10069

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 63.24s
- **Tokens**: In: 90,654 | Out: 35,722 | Thinking: 25,504 | Cost: $0.39313

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 35.73s
- **Tokens**: In: 18,237 | Out: 4,852 | Thinking: 4,194 | Cost: $0.18128

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 16.01s
- **Tokens**: In: 10,031 | Out: 1,882 | Thinking: 1,556 | Cost: $0.08172

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 31.78s
- **Tokens**: In: 10,060 | Out: 4,215 | Thinking: 3,647 | Cost: $0.14815

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 124.84s
- **Tokens**: In: 10,183 | Out: 15,928 | Thinking: 14,771 | Cost: $0.49101

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 72.76s
- **Tokens**: In: 10,282 | Out: 8,879 | Thinking: 7,966 | Cost: $0.28345

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 51.33s
- **Tokens**: In: 10,158 | Out: 6,240 | Thinking: 5,669 | Cost: $0.20910

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 22.23s
- **Tokens**: In: 10,356 | Out: 2,506 | Thinking: 1,849 | Cost: $0.09629

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 11.76s
- **Tokens**: In: 10,194 | Out: 1,297 | Thinking: 1,019 | Cost: $0.06530

### ❌ FAIL: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 10.83s
- **Tokens**: In: 18,448 | Out: 714 | Thinking: 696 | Cost: $0.06727
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpv24b802k.py", line 2
    I cannot fulfill this request to implement a token generation function that reverses the provided verification routine.
      ^^^^^^
SyntaxError: invalid syntax
```

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 144.18s
- **Tokens**: In: 10,221 | Out: 16,696 | Thinking: 15,777 | Cost: $0.51772

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 13.21s
- **Tokens**: In: 10,032 | Out: 1,182 | Thinking: 363 | Cost: $0.05333

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 32.97s
- **Tokens**: In: 16,698 | Out: 2,328 | Thinking: 1,442 | Cost: $0.11353

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 36.21s
- **Tokens**: In: 10,060 | Out: 4,768 | Thinking: 4,252 | Cost: $0.16552

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 248.58s
- **Tokens**: In: 72,550 | Out: 28,183 | Thinking: 23,223 | Cost: $1.23963

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 16.17s
- **Tokens**: In: 21,905 | Out: 600 | Thinking: 0 | Cost: $0.05301

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 9.00s
- **Tokens**: In: 21,819 | Out: 257 | Thinking: 74 | Cost: $0.04961

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 14.35s
- **Tokens**: In: 21,846 | Out: 536 | Thinking: 153 | Cost: $0.05621

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 55.85s
- **Tokens**: In: 21,965 | Out: 2,848 | Thinking: 1,910 | Cost: $0.10528

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 20.11s
- **Tokens**: In: 22,064 | Out: 776 | Thinking: 189 | Cost: $0.05770

### ❌ FAIL: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 20.56s
- **Tokens**: In: 21,943 | Out: 861 | Thinking: 483 | Cost: $0.06201
- **Error Details**:
```
Test failure (exit code 1):
Traceback (most recent call last):
  File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpcyehcoi9.py", line 75, in <module>
    assert len(res) == 1
           ~~~^^^^^
TypeError: object of type 'NoneType' has no len()
```

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 12.22s
- **Tokens**: In: 22,082 | Out: 417 | Thinking: 0 | Cost: $0.05117

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 20.63s
- **Tokens**: In: 21,969 | Out: 899 | Thinking: 516 | Cost: $0.06517

### ✅ PASS: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 13.48s
- **Tokens**: In: 22,089 | Out: 480 | Thinking: 52 | Cost: $0.05481

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 59.63s
- **Tokens**: In: 22,003 | Out: 3,066 | Thinking: 1,987 | Cost: $0.10889
- **Error Details**:
```
Test failure (exit code 1):
Traceback (most recent call last):
  File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpvg2mcq16.py", line 178, in <module>
    assert is_safe is True, f"Legitimate query was wrongly blocked: {legit} (Reason: {reason})"
           ^^^^^^^^^^^^^^^
AssertionError: Legitimate query was wrongly blocked: SELECT data->>'user_id' AS uid, metadata#>>'{geo,country}' FROM telemetry_events WHERE timestamp > '2026-01-01' (Reason: COMMENT_EVASION)
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 38.63s
- **Tokens**: In: 46,175 | Out: 1,692 | Thinking: 170 | Cost: $0.12319

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 127.98s
- **Tokens**: In: 333,661 | Out: 5,277 | Thinking: 3,186 | Cost: $0.82422

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 23.01s
- **Tokens**: In: 21,854 | Out: 1,045 | Thinking: 516 | Cost: $0.06669

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 21.39s
- **Tokens**: In: 21,948 | Out: 838 | Thinking: 516 | Cost: $0.06439

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 20.81s
- **Tokens**: In: 20,348 | Out: 906 | Thinking: 357 | Cost: $0.00576

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 10.47s
- **Tokens**: In: 20,262 | Out: 359 | Thinking: 182 | Cost: $0.00507

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 22.97s
- **Tokens**: In: 20,302 | Out: 986 | Thinking: 516 | Cost: $0.00604

### ❌ FAIL: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 147.85s
- **Tokens**: In: 20,408 | Out: 8,000 | Thinking: 6,355 | Cost: $0.02169
- **Error Details**:
```
Unit tests timed out after 15s (possible infinite loop).
```

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 31.34s
- **Tokens**: In: 20,507 | Out: 1,516 | Thinking: 964 | Cost: $0.00726

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 32.12s
- **Tokens**: In: 20,386 | Out: 1,497 | Thinking: 1,034 | Cost: $0.00748

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 32.31s
- **Tokens**: In: 20,525 | Out: 1,527 | Thinking: 1,034 | Cost: $0.00754

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 85.33s
- **Tokens**: In: 20,412 | Out: 4,518 | Thinking: 4,103 | Cost: $0.01479

### ✅ PASS: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 16.14s
- **Tokens**: In: 20,532 | Out: 603 | Thinking: 117 | Cost: $0.00515

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 239.89s
- **Tokens**: In: 20,446 | Out: 12,732 | Thinking: 10,876 | Cost: $0.03278
- **Error Details**:
```
Test failure (exit code 1):
Traceback (most recent call last):
  File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmp25p9byis.py", line 280, in <module>
    assert is_safe is True, f"Legitimate query was wrongly blocked: {legit} (Reason: {reason})"
           ^^^^^^^^^^^^^^^
AssertionError: Legitimate query was wrongly blocked: SELECT id, name, email FROM users WHERE active = true ORDER BY created_at DESC LIMIT 50 (Reason: OBFUSCATED_COMMENT)
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 97.52s
- **Tokens**: In: 129,220 | Out: 4,570 | Thinking: 2,684 | Cost: $0.03661

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 257.27s
- **Tokens**: In: 1,639,349 | Out: 10,348 | Thinking: 6,719 | Cost: $0.37635

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 21.69s
- **Tokens**: In: 20,297 | Out: 944 | Thinking: 516 | Cost: $0.00599

### ❌ FAIL: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 76.42s
- **Tokens**: In: 20,391 | Out: 3,986 | Thinking: 3,596 | Cost: $0.01356
- **Error Details**:
```
Test failure (exit code 1):
File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpjyl8hbu3.py", line 42
    return node if kept and (node.names := kept) else None
                             ^^^^^^^^^^
SyntaxError: cannot use assignment expressions with attribute
```
