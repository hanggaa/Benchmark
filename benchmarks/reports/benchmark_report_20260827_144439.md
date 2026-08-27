# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **2** model configuration(s) across **6** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.7 Flash (High)** | `agy` | `-` | **100.0%** (3/3) | 16.3s | 7,692 | $0.10955 | **873** |
| **Gemini 3.5 Flash (High)** | `agy` | `-` | **100.0%** (3/3) | 15.07s | 16,021 | $0.19903 | **490** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Bugfix | Logic | Research |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `default` | 100% (1/1) | 100% (1/1) | 100% (1/1) |
| **Gemini 3.5 Flash (High)** | `agy` | `default` | 100% (1/1) | 100% (1/1) | 100% (1/1) |

## 📝 Detailed Test Execution Logs

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.7 Flash (High)` via `agy`
- **Duration**: 15.37s
- **Tokens**: In: 17,935 | Out: 5,041 | Thinking: 4,222 | Cost: $0.04572

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.7 Flash (High)` via `agy`
- **Duration**: 21.66s
- **Tokens**: In: 18,168 | Out: 2,991 | Thinking: 2,210 | Cost: $0.03377

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.7 Flash (High)` via `agy`
- **Duration**: 11.87s
- **Tokens**: In: 17,855 | Out: 2,807 | Thinking: 1,260 | Cost: $0.03006

### ✅ PASS: Thread-Safe LRU Cache with TTL & Eviction (`logic_01_lru_ttl`)
- **Model**: `Gemini 3.5 Flash (High)` via `agy`
- **Duration**: 21.62s
- **Tokens**: In: 17,937 | Out: 9,348 | Thinking: 8,382 | Cost: $0.07113

### ✅ PASS: Fix JWT Verification Security Vulnerabilities (`bugfix_01_jwt_verifier`)
- **Model**: `Gemini 3.5 Flash (High)` via `agy`
- **Duration**: 14.46s
- **Tokens**: In: 47,528 | Out: 7,498 | Thinking: 4,746 | Cost: $0.08936

### ✅ PASS: PRD Generation with Strict Handoff Context (`research_01_prd_structure`)
- **Model**: `Gemini 3.5 Flash (High)` via `agy`
- **Duration**: 9.14s
- **Tokens**: In: 17,855 | Out: 4,003 | Thinking: 2,893 | Cost: $0.03854
