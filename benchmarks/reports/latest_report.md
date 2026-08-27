# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **4** model configuration(s) across **36** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | **100.0%** (9/9) | 10.23s | 20,004 | $0.05504 | **1,666** |
| **Gemini 3.5 Flash (High)** | `agy` | `high` | **100.0%** (9/9) | 27.4s | 65,600 | $0.17469 | **556** |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | **100.0%** (9/9) | 28.58s | 71,977 | $0.19410 | **502** |
| **Gemini 3.1 Pro (High)** | `agy` | `high` | **100.0%** (9/9) | 31.1s | 24,006 | $0.53606 | **185** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Bugfix | Logic | Research | Tool_use |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `high` | 100% (2/2) | 100% (4/4) | 100% (2/2) | 100% (1/1) |
| **Gemini 3.6 Flash (High)** | `agy` | `high` | 100% (2/2) | 100% (4/4) | 100% (2/2) | 100% (1/1) |
| **Gemini 3.5 Flash (High)** | `agy` | `high` | 100% (2/2) | 100% (4/4) | 100% (2/2) | 100% (1/1) |
| **Gemini 3.1 Pro (High)** | `agy` | `high` | 100% (2/2) | 100% (4/4) | 100% (2/2) | 100% (1/1) |

## 📝 Detailed Test Execution Logs

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.73s
- **Tokens**: In: 17,928 | Out: 3,785 | Thinking: 2,915 | Cost: $0.00671

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 8.94s
- **Tokens**: In: 17,841 | Out: 2,998 | Thinking: 2,547 | Cost: $0.00600

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.99s
- **Tokens**: In: 17,872 | Out: 2,431 | Thinking: 1,896 | Cost: $0.00528

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 17.60s
- **Tokens**: In: 17,993 | Out: 6,633 | Thinking: 5,191 | Cost: $0.00979

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 6.86s
- **Tokens**: In: 18,171 | Out: 2,009 | Thinking: 1,265 | Cost: $0.00469

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.19s
- **Tokens**: In: 23,840 | Out: 1,792 | Thinking: 886 | Cost: $0.00640

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 9.62s
- **Tokens**: In: 17,853 | Out: 2,288 | Thinking: 1,128 | Cost: $0.00473

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 12.78s
- **Tokens**: In: 17,803 | Out: 3,035 | Thinking: 1,913 | Cost: $0.00564

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.7 Flash (High)` [high] via `agy`
- **Duration**: 7.32s
- **Tokens**: In: 17,872 | Out: 2,929 | Thinking: 2,263 | Cost: $0.00580

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 27.93s
- **Tokens**: In: 40,077 | Out: 15,025 | Thinking: 10,476 | Cost: $0.02407

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 8.82s
- **Tokens**: In: 17,373 | Out: 4,923 | Thinking: 3,773 | Cost: $0.00874

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 22.10s
- **Tokens**: In: 30,856 | Out: 12,975 | Thinking: 9,956 | Cost: $0.02129

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 70.25s
- **Tokens**: In: 109,345 | Out: 21,349 | Thinking: 10,034 | Cost: $0.05677

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 10.31s
- **Tokens**: In: 11,280 | Out: 6,936 | Thinking: 6,220 | Cost: $0.00989

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 46.14s
- **Tokens**: In: 42,774 | Out: 9,725 | Thinking: 6,903 | Cost: $0.02204

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 8.72s
- **Tokens**: In: 10,971 | Out: 4,155 | Thinking: 3,037 | Cost: $0.00627

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 28.62s
- **Tokens**: In: 21,123 | Out: 6,940 | Thinking: 4,095 | Cost: $0.01147

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.6 Flash (High)` [high] via `agy`
- **Duration**: 34.34s
- **Tokens**: In: 43,661 | Out: 20,648 | Thinking: 17,483 | Cost: $0.03356

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 20.81s
- **Tokens**: In: 30,604 | Out: 9,039 | Thinking: 6,766 | Cost: $0.01545

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 9.40s
- **Tokens**: In: 17,841 | Out: 4,963 | Thinking: 4,557 | Cost: $0.00839

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 7.18s
- **Tokens**: In: 17,874 | Out: 4,004 | Thinking: 3,518 | Cost: $0.00719

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 54.22s
- **Tokens**: In: 71,344 | Out: 23,183 | Thinking: 16,002 | Cost: $0.04003

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 27.46s
- **Tokens**: In: 49,004 | Out: 13,011 | Thinking: 9,383 | Cost: $0.02430

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 15.68s
- **Tokens**: In: 51,206 | Out: 4,548 | Thinking: 2,687 | Cost: $0.01401

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 18.60s
- **Tokens**: In: 17,328 | Out: 8,183 | Thinking: 5,514 | Cost: $0.01173

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 79.01s
- **Tokens**: In: 118,828 | Out: 15,133 | Thinking: 10,110 | Cost: $0.04199

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.5 Flash (High)` [high] via `agy`
- **Duration**: 14.26s
- **Tokens**: In: 17,876 | Out: 7,808 | Thinking: 7,063 | Cost: $0.01160

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 27.22s
- **Tokens**: In: 18,197 | Out: 3,485 | Thinking: 2,767 | Cost: $0.06481

### ✅ PASS: Topological Batch Scheduler with Cycle Detection (`logic_02_topo_cycle`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 25.50s
- **Tokens**: In: 9,994 | Out: 2,932 | Thinking: 2,565 | Cost: $0.05102

### ✅ PASS: Sliding Window Log Rate Limiter (`logic_03_sliding_rate_limiter`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 22.92s
- **Tokens**: In: 10,032 | Out: 2,680 | Thinking: 2,096 | Cost: $0.04675

### ✅ PASS: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 82.26s
- **Tokens**: In: 10,151 | Out: 9,724 | Thinking: 8,622 | Cost: $0.12835

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 32.57s
- **Tokens**: In: 10,317 | Out: 4,088 | Thinking: 3,412 | Cost: $0.06352

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 23.06s
- **Tokens**: In: 20,115 | Out: 1,621 | Thinking: 587 | Cost: $0.06472

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 18.95s
- **Tokens**: In: 10,008 | Out: 1,773 | Thinking: 849 | Cost: $0.03379

### ✅ PASS: Vector Database Tradeoff & Pricing Comparison Matrix (`research_02_database_tradeoff`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 30.71s
- **Tokens**: In: 9,959 | Out: 2,809 | Thinking: 1,537 | Cost: $0.04406

### ✅ PASS: Surgical Connection Pool with Auto-Reconnection (`tool_01_surgical_refactor`)
- **Model**: `Gemini 3.1 Pro (High)` [high] via `agy`
- **Duration**: 16.74s
- **Tokens**: In: 10,028 | Out: 1,926 | Thinking: 1,571 | Cost: $0.03907
