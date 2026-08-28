# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **6** model configuration(s) across **84** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **gpt-5.6-terra** | `codex` | `high` | **100.0%** (14/14) | 39.16s | 13,794 | $2.28780 | **44** |
| **Gemini 3.1 Pro (High)** | `agy` | `high` | **100.0%** (14/14) | 59.54s | 73,399 | $3.27934 | **30** |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | **92.9%** (13/14) | 31.28s | 73,960 | $1.39120 | **62** |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | **92.9%** (13/14) | 30.39s | 136,635 | $2.03762 | **42** |
| **Gemini 3.5 Flash (High)** | `agy` | `high` | **92.9%** (13/14) | 38.08s | 153,500 | $2.40062 | **36** |
| **gpt-5.6-luna** | `codex` | `high` | **85.7%** (12/14) | 80.24s | 33,096 | $0.14773 | **362** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Bugfix | Logic | Research | Tool_use |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | 100% (4/4) | 83% (5/6) | 100% (2/2) | 100% (2/2) |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | 75% (3/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **Gemini 3.5 Flash (High)** | `agy` | `high` | 100% (4/4) | 100% (6/6) | 50% (1/2) | 100% (2/2) |
| **Gemini 3.1 Pro (High)** | `agy` | `high` | 100% (4/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **gpt-5.6-terra** | `codex` | `high` | 100% (4/4) | 100% (6/6) | 100% (2/2) | 100% (2/2) |
| **gpt-5.6-luna** | `codex` | `high` | 100% (4/4) | 83% (5/6) | 50% (1/2) | 100% (2/2) |

## 📝 Detailed Test Execution Logs

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 11.40s
- **Tokens**: In: 17,931 | Out: 4,595 | Thinking: 3,702 | Cost: $0.04456

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.49s
- **Tokens**: In: 17,845 | Out: 3,280 | Thinking: 2,779 | Cost: $0.03610

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 5.81s
- **Tokens**: In: 17,882 | Out: 2,289 | Thinking: 1,617 | Cost: $0.02806

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 19.30s
- **Tokens**: In: 18,001 | Out: 7,930 | Thinking: 6,653 | Cost: $0.06819

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 16.19s
- **Tokens**: In: 18,100 | Out: 4,879 | Thinking: 3,937 | Cost: $0.04664

### ❌ FAIL: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 26.23s
- **Tokens**: In: 17,972 | Out: 7,220 | Thinking: 6,357 | Cost: $0.06439
- **Error Details**:
```
Test failure (exit code 1):
Traceback (most recent call last):
  File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpor_p1brc.py", line 102, in <module>
    res = parser.feed(pkt1)
  File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmpor_p1brc.py", line 78, in feed
    del self._buffer[:total_frame_size]
        ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
BufferError: Existing exports of data: object cannot be re-sized
```

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 8.07s
- **Tokens**: In: 18,166 | Out: 3,358 | Thinking: 2,636 | Cost: $0.03610

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 7.27s
- **Tokens**: In: 21,259 | Out: 1,969 | Thinking: 1,025 | Cost: $0.03023

### ✅ PASS: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 19.53s
- **Tokens**: In: 18,139 | Out: 2,267 | Thinking: 1,681 | Cost: $0.02841

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 171.51s
- **Tokens**: In: 136,796 | Out: 56,517 | Thinking: 19,748 | Cost: $0.56903

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 8.50s
- **Tokens**: In: 17,850 | Out: 2,241 | Thinking: 1,291 | Cost: $0.02663

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 14.81s
- **Tokens**: In: 17,813 | Out: 3,933 | Thinking: 1,891 | Cost: $0.03520

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 8.29s
- **Tokens**: In: 17,876 | Out: 3,540 | Thinking: 3,053 | Cost: $0.03813

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 111.58s
- **Tokens**: In: 95,663 | Out: 28,374 | Thinking: 17,590 | Cost: $0.33953

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 13.77s
- **Tokens**: In: 19,200 | Out: 8,096 | Thinking: 7,314 | Cost: $0.07219

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 5.30s
- **Tokens**: In: 10,959 | Out: 3,408 | Thinking: 3,037 | Cost: $0.03392

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 17.17s
- **Tokens**: In: 37,926 | Out: 8,550 | Thinking: 4,370 | Cost: $0.10668

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 49.68s
- **Tokens**: In: 95,598 | Out: 26,652 | Thinking: 14,761 | Cost: $0.28663

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 23.50s
- **Tokens**: In: 28,443 | Out: 15,116 | Thinking: 13,124 | Cost: $0.13182

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 21.16s
- **Tokens**: In: 25,105 | Out: 11,851 | Thinking: 9,359 | Cost: $0.10754

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 17.73s
- **Tokens**: In: 24,995 | Out: 9,795 | Thinking: 7,326 | Cost: $0.09212

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 17.55s
- **Tokens**: In: 18,754 | Out: 4,420 | Thinking: 3,176 | Cost: $0.05095

### ✅ PASS: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 15.10s
- **Tokens**: In: 3,757 | Out: 3,616 | Thinking: 3,046 | Cost: $0.03073

### ❌ FAIL: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 83.42s
- **Tokens**: In: 87,985 | Out: 35,562 | Thinking: 20,727 | Cost: $0.36579
- **Error Details**:
```
Test failure (exit code 1):
Traceback (most recent call last):
  File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmp7_ivctre.py", line 206, in <module>
    assert is_safe is True, f"Legitimate query was wrongly blocked: {legit} (Reason: {reason})"
           ^^^^^^^^^^^^^^^
AssertionError: Legitimate query was wrongly blocked: SELECT * FROM shipments WHERE status = 'delayed' AND carrier = 'orbital_express' (Reason: Boolean/Tautology injection)
```

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 10.55s
- **Tokens**: In: 17,206 | Out: 4,659 | Thinking: 2,025 | Cost: $0.04255

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 29.56s
- **Tokens**: In: 22,758 | Out: 5,932 | Thinking: 2,902 | Cost: $0.05860

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 26.59s
- **Tokens**: In: 34,352 | Out: 16,704 | Thinking: 14,849 | Cost: $0.15403

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 94.42s
- **Tokens**: In: 100,652 | Out: 42,094 | Thinking: 30,619 | Cost: $0.50406

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 14.12s
- **Tokens**: In: 17,929 | Out: 7,375 | Thinking: 6,674 | Cost: $0.06613

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 8.84s
- **Tokens**: In: 17,839 | Out: 4,573 | Thinking: 4,152 | Cost: $0.04610

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 9.04s
- **Tokens**: In: 17,880 | Out: 4,365 | Thinking: 3,908 | Cost: $0.04443

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 29.18s
- **Tokens**: In: 17,997 | Out: 16,404 | Thinking: 15,105 | Cost: $0.13166

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 33.05s
- **Tokens**: In: 67,044 | Out: 16,646 | Thinking: 14,206 | Cost: $0.16904

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 34.99s
- **Tokens**: In: 106,573 | Out: 16,267 | Thinking: 11,574 | Cost: $0.19885

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 37.50s
- **Tokens**: In: 65,113 | Out: 14,661 | Thinking: 11,713 | Cost: $0.16227

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 15.52s
- **Tokens**: In: 34,205 | Out: 5,160 | Thinking: 3,139 | Cost: $0.06975

### ✅ PASS: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 7.85s
- **Tokens**: In: 18,143 | Out: 3,368 | Thinking: 2,729 | Cost: $0.03647

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 92.89s
- **Tokens**: In: 127,627 | Out: 40,578 | Thinking: 29,946 | Cost: $0.42291

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 4.68s
- **Tokens**: In: 17,857 | Out: 1,968 | Thinking: 1,233 | Cost: $0.02540

### ❌ FAIL: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 74.10s
- **Tokens**: In: 118,474 | Out: 12,780 | Thinking: 10,200 | Cost: $0.20636
- **Error Details**:
```
Missing required heading: 'Recommendation Matrix'
Missing required content/keyword: '| Engine |'
Missing required content/keyword: '$'
```

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 28.55s
- **Tokens**: In: 29,206 | Out: 9,058 | Thinking: 8,471 | Cost: $0.09528

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 142.78s
- **Tokens**: In: 188,502 | Out: 42,423 | Thinking: 30,450 | Cost: $0.72597

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 52.16s
- **Tokens**: In: 18,204 | Out: 6,264 | Thinking: 5,622 | Cost: $0.22380

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 26.86s
- **Tokens**: In: 10,001 | Out: 3,053 | Thinking: 2,647 | Cost: $0.11557

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 21.56s
- **Tokens**: In: 10,035 | Out: 2,274 | Thinking: 1,719 | Cost: $0.09005

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 94.80s
- **Tokens**: In: 10,155 | Out: 11,155 | Thinking: 10,283 | Cost: $0.35203

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 59.40s
- **Tokens**: In: 10,249 | Out: 6,939 | Thinking: 6,292 | Cost: $0.22916

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 80.26s
- **Tokens**: In: 10,127 | Out: 8,548 | Thinking: 7,831 | Cost: $0.27607

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 23.05s
- **Tokens**: In: 10,320 | Out: 2,675 | Thinking: 2,159 | Cost: $0.10338

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 26.23s
- **Tokens**: In: 17,333 | Out: 2,068 | Thinking: 1,299 | Cost: $0.11920

### ✅ PASS: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 22.38s
- **Tokens**: In: 10,302 | Out: 2,753 | Thinking: 1,930 | Cost: $0.10107

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 127.41s
- **Tokens**: In: 10,195 | Out: 14,027 | Thinking: 13,402 | Cost: $0.44200

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 24.20s
- **Tokens**: In: 18,115 | Out: 2,377 | Thinking: 1,482 | Cost: $0.10317

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 27.89s
- **Tokens**: In: 9,963 | Out: 2,494 | Thinking: 1,448 | Cost: $0.08911

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 16.99s
- **Tokens**: In: 10,029 | Out: 1,690 | Thinking: 1,367 | Cost: $0.07600

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 230.30s
- **Tokens**: In: 68,402 | Out: 22,886 | Thinking: 15,918 | Cost: $0.95872

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 15.12s
- **Tokens**: In: 21,086 | Out: 586 | Thinking: 0 | Cost: $0.05120

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 9.86s
- **Tokens**: In: 21,000 | Out: 268 | Thinking: 94 | Cost: $0.04834

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 14.55s
- **Tokens**: In: 21,027 | Out: 534 | Thinking: 153 | Cost: $0.05230

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 31.47s
- **Tokens**: In: 21,146 | Out: 1,462 | Thinking: 516 | Cost: $0.07007

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 19.08s
- **Tokens**: In: 21,245 | Out: 824 | Thinking: 276 | Cost: $0.05769

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 21.47s
- **Tokens**: In: 21,124 | Out: 909 | Thinking: 516 | Cost: $0.06134

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 19.22s
- **Tokens**: In: 21,263 | Out: 826 | Thinking: 348 | Cost: $0.05861

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 47.04s
- **Tokens**: In: 21,150 | Out: 2,300 | Thinking: 1,894 | Cost: $0.09667

### ✅ PASS: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 15.00s
- **Tokens**: In: 21,270 | Out: 595 | Thinking: 165 | Cost: $0.05570

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 100.39s
- **Tokens**: In: 21,184 | Out: 5,311 | Thinking: 3,624 | Cost: $0.15363

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 40.66s
- **Tokens**: In: 97,751 | Out: 1,681 | Thinking: 141 | Cost: $0.23109

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 171.12s
- **Tokens**: In: 498,613 | Out: 7,265 | Thinking: 5,127 | Cost: $1.22877

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 19.99s
- **Tokens**: In: 21,035 | Out: 827 | Thinking: 424 | Cost: $0.05908

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `gpt-5.6-terra` [high] via `codex`
- **Duration**: 23.27s
- **Tokens**: In: 21,129 | Out: 917 | Thinking: 516 | Cost: $0.06329

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 29.58s
- **Tokens**: In: 19,528 | Out: 1,323 | Thinking: 754 | Cost: $0.00658

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 10.51s
- **Tokens**: In: 19,442 | Out: 364 | Thinking: 108 | Cost: $0.00463

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 14.88s
- **Tokens**: In: 19,469 | Out: 549 | Thinking: 177 | Cost: $0.00494

### ❌ FAIL: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 174.55s
- **Tokens**: In: 19,588 | Out: 9,459 | Thinking: 7,510 | Cost: $0.02446
- **Error Details**:
```
Unit tests timed out after 15s (possible infinite loop).
```

### ✅ PASS: Distributed Consensus: Quorum State Machine & Split-Brain Handler (`logic_05_raft_quorum`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 55.16s
- **Tokens**: In: 19,687 | Out: 2,652 | Thinking: 2,070 | Cost: $0.00997

### ✅ PASS: Zero-Copy Streaming Binary Packet Frame Parser with CRC32 (`logic_06_zero_copy_parser`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 50.41s
- **Tokens**: In: 19,566 | Out: 2,479 | Thinking: 2,070 | Cost: $0.00974

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 22.56s
- **Tokens**: In: 19,705 | Out: 983 | Thinking: 516 | Cost: $0.00610

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 82.44s
- **Tokens**: In: 19,592 | Out: 4,359 | Thinking: 4,021 | Cost: $0.01415

### ✅ PASS: Cryptographic Inverse: Mathematical Token Invertor & Verification Algorithm (`sec_ctf_01_keygen`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 15.97s
- **Tokens**: In: 19,712 | Out: 648 | Thinking: 146 | Cost: $0.00526

### ✅ PASS: CTF / Security: SQL Injection AST Firewall & Payload Interceptor (`sec_ctf_02_sql_ast_firewall`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 208.04s
- **Tokens**: In: 19,626 | Out: 11,349 | Thinking: 10,358 | Cost: $0.03015

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 36.58s
- **Tokens**: In: 19,457 | Out: 1,755 | Thinking: 45 | Cost: $0.00623

### ❌ FAIL: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 300.01s
- **Tokens**: In: 15,500 | Out: 0 | Thinking: 0 | Cost: $0.00310
- **Error Details**:
```
TIMEOUT: Process exceeded 300s limit
```

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 23.77s
- **Tokens**: In: 19,477 | Out: 1,056 | Thinking: 516 | Cost: $0.00615

### ✅ PASS: AST-Based Surgical Code Refactoring & Dead Import Pruner (`tool_02_ast_pruner`)
- **Model**: `gpt-5.6-luna` [high] via `codex`
- **Duration**: 98.90s
- **Tokens**: In: 19,571 | Out: 5,188 | Thinking: 4,805 | Cost: $0.01627
