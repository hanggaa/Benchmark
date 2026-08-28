# 🧪 Personal LLM Benchmark Suite

Framework pengujian benchmark otomatis untuk mengevaluasi model-model LLM pada CLI Agent (*Antigravity CLI, Codex CLI, OpenCode CLI, Claude Code CLI*) dengan metrik objektif, unit test tersembunyi, dan telemetri token riil.

Mengukur performa secara empiris berdasarkan **4 Pilar Utama**:
1. **Deterministic Accuracy (Pass@1)** — Unit test tersembunyi (`pytest`/`unittest`) dan validasi skema struktur/JSON tanpa risiko kontaminasi benchmark publik.
2. **Token Economics & Reasoning Efficiency** — Input tokens, Output tokens, Thinking/Reasoning tokens, dan estimasi biaya riil ($).
3. **Speed & Latency** — Rata-rata durasi eksekusi per soal (detik).
4. **Value / Efficiency Score** — Rasio kepintaran terhadap biaya (`Pass Rate (%) / Cost ($)`).

---

## 📁 Struktur Direktori

```text
benchmarks/
├── cases/                     # Kumpulan 9 skenario pengujian & hidden tests
│   ├── cat_a_logic/           # Algoritma, LRU Cache TTL, Topo DAG, Async Worker Pool
│   ├── cat_b_bugfix/          # Perbaikan bug keamanan JWT & ReDoS Linearization
│   ├── cat_c_research/        # Validasi struktur PRD & Matrix DB Tradeoffs
│   └── cat_d_tool_use/        # Refactoring Surgical Connection Pool
├── evaluators/
│   ├── __init__.py
│   └── evaluators.py          # UnitTestEvaluator (isolated sandbox) & SchemaEvaluator
├── runners/
│   ├── base_runner.py         # Abstract base runner & pricing engine
│   ├── antigravity_runner.py  # Driver untuk Antigravity CLI (agy)
│   ├── codex_runner.py        # Driver untuk Codex CLI (codex)
│   ├── opencode_runner.py     # Driver untuk OpenCode CLI (opencode)
│   └── claude_runner.py       # Driver untuk Claude Code CLI (claude)
├── reports/                   # Laporan Markdown (latest_report.md) & log data JSON
├── config.json                # Konfigurasi pricing per 1M token & CLI settings
├── models.py                  # Dataclass TestCase, BenchmarkResult, TokenUsage
├── runner.py                  # CLI Orchestrator dengan Smart Auto-Routing
└── README.md                  # Dokumentasi & panduan penggunaan
```

---

## 🧠 Smart Model-to-CLI Auto-Routing

Runner dilengkapi sistem **Auto-Detection Pintar**. Anda bisa memasukkan daftar model campuran dari berbagai provider dalam satu kali perintah, dan runner akan secara otomatis mengarahkan masing-masing model ke CLI yang tepat:

| Pola Nama Model | Target CLI Adapter | Contoh Model |
| :--- | :--- | :--- |
| `Gemini ...` / `gemini-...` | **Antigravity CLI (`agy`)** | `Gemini 3.7 Flash (High)`, `Gemini 3.1 Pro (High)` |
| `gpt-...`, `o1...`, `o3...` | **Codex CLI (`codex`)** | `gpt-5.6-sol`, `o3-mini`, `gpt-4o` |
| `opencode/...`, `bailian-...`, `deepseek...` | **OpenCode CLI (`opencode`)** | `opencode/deepseek-v4-flash-free`, `bailian-token-plan-personal/qwen3.7-max` |
| `claude-...` | **Claude Code CLI (`claude`)** | `claude-3-7-sonnet`, `claude-3-5-haiku` |

> [!TIP]
> **Prefix Eksplisit:** Anda juga bisa menentukan CLI secara manual menggunakan format `cli:model` (contoh: `codex:gpt-5.6-sol`, `agy:Gemini 3.7 Flash (High)`, `opencode:opencode/deepseek-v4-flash-free`).

---

## ⚡ Cara Menentukan Reasoning Effort (`high`, `medium`, `low`)

Anda memiliki beberapa cara fleksibel untuk mengatur *thinking/reasoning effort*:

### 1. Mengatur Effort Global untuk Semua Model
Gunakan flag `--effort`:
```bash
python3 -m benchmarks.runner \
  --models "Gemini 3.7 Flash (High), gpt-5.6-sol" \
  --effort high
```

### 2. Mengatur Effort Spesifik per Model (Inline Syntax)
Gunakan opsi `--effort <level>` di dalam string model:
```bash
python3 -m benchmarks.runner \
  --models "Gemini 3.7 Flash (High), gpt-5.6-sol --effort high, o3-mini --effort medium"
```

### 3. Menggunakan Format Prefix Titik Dua (`cli:model:effort`)
```bash
python3 -m benchmarks.runner \
  --models "codex:gpt-5.6-sol:high, agy:Gemini 3.7 Flash (High), codex:o3-mini:medium"
```

---

## 🚀 Panduan Eksekusi Benchmark

### 1. Dry Run (Melihat Execution Plan & Daftar Soal Tanpa Menghabiskan Token)
Gunakan flag `--dry-run` untuk memverifikasi CLI mana yang akan menangani tiap model:
```bash
python3 -m benchmarks.runner \
  --models "Gemini 3.7 Flash (High), Gemini 3.6 Flash (High), gpt-5.6-sol --effort high, opencode/deepseek-v4-flash-free" \
  --dry-run
```

---

### 2. Pengujian Campuran Lintas CLI Sekaligus (Multi-Model & Multi-CLI)
Jalankan benchmark untuk model Antigravity, Codex, dan OpenCode dalam satu perintah:
```bash
python3 -m benchmarks.runner \
  --models "Gemini 3.7 Flash (High), gpt-5.6-sol --effort high, opencode/deepseek-v4-flash-free"
```

---

### 3. Membandingkan Beberapa Varian Model di Antigravity CLI Saja
```bash
python3 -m benchmarks.runner \
  --cli agy \
  --models "Gemini 3.7 Flash (High), Gemini 3.6 Flash (High), Gemini 3.5 Flash (High), Gemini 3.1 Pro (High)"
```

---

### 4. Memfilter Berdasarkan Kategori Soal Tertentu
Hanya menguji kategori tertentu untuk mempercepat evaluasi:
```bash
# Hanya kategori Logika & Algoritma
python3 -m benchmarks.runner \
  --models "Gemini 3.7 Flash (High), gpt-5.6-sol --effort high" \
  --category logic

# Kategori Bugfix & Deep Research
python3 -m benchmarks.runner \
  --models "Gemini 3.7 Flash (High), gpt-5.6-sol --effort high" \
  --category bugfix,research
```

---

### 5. Menguji Hanya 1 Kasus Uji Spesifik (Single Case Testing)
Gunakan flag `--case <case_id>`:
```bash
python3 -m benchmarks.runner \
  --models "Gemini 3.7 Flash (High), gpt-5.6-sol --effort high" \
  --case logic_04_async_worker_pool
```

---

## 📋 Daftar 14 Skenario Kasus Uji Bawaan

| ID Kasus | Kategori | Tingkat Kesulitan | Aspek Kritis yang Diuji |
| :--- | :--- | :---: | :--- |
| `logic_01_lru_ttl` | Logic & Algo | Hard | Thread-safe LRU Cache, TTL Expiration, Multi-thread Concurrency |
| `logic_02_topo_cycle` | Logic & Algo | Medium | Topological DAG Batching & Circular Dependency Detection |
| `logic_03_sliding_rate_limiter` | Logic & Algo | Medium | Sliding Window Log Rate Limiter & Boundary Calculation |
| `logic_04_async_worker_pool` | Logic & Algo | Hard | `asyncio` Priority Worker Pool, Graceful Drain & Cancel |
| `logic_05_raft_quorum` | Logic & Algo | Hard | Distributed Quorum State Machine, Minority Reject & Split-Brain |
| `logic_06_zero_copy_parser` | Logic & Algo | Hard | Zero-Copy Streaming Binary Frame Parser, Fragments & CRC32 |
| `bugfix_01_jwt_verifier` | Bugfix / Sec | Medium | JWT `none` Algorithm Attack & Exact Expiration Boundary |
| `bugfix_02_redos_defense` | Bugfix / Sec | Hard | Catastrophic ReDoS Backtracking Attack & Linearization ($O(N)$) |
| `sec_ctf_01_keygen` | CTF / Security | Hard | Reverse Engineering Obfuscated Bitwise Hash & License Keygen |
| `sec_ctf_02_sql_ast_firewall` | CTF / Security | Hard | Zero-Day SQLi Payload Interceptor & AST False-Positive Immunity |
| `research_01_prd_structure` | Research / Doc | Medium | PRD Schema Validation & Exact `## Handoff Context` Block |
| `research_02_database_tradeoff` | Research / Doc | Medium | Vector DB 10M Matrix (pgvector vs Qdrant vs Pinecone) |
| `tool_01_surgical_refactor` | Tool Use | Medium | Surgical Connection Pool Healthcheck & Signature Parity |
| `tool_02_ast_pruner` | Tool Use | Hard | AST Dead Import Pruning, Private Function Stripping & Docstring Preservation |

---

## 🌐 Live Web Dashboard & Deployment

Setiap kali benchmark selesai dijalankan, runner secara otomatis memperbarui data di:
* `benchmarks/reports/latest_report.md` (Laporan Leaderboard Markdown)
* `src/data/benchmark-data.json` (Data mentah untuk Dashboard Web)

### Menjalankan Dashboard di Local
```bash
npm run dev
```

### Deploy ke GitHub Pages (`benchmarks.hanggaa.xyz`)
```bash
npm run deploy
```

---

## ➕ Cara Menambahkan Skenario Uji Baru

Buat file JSON baru di dalam folder `benchmarks/cases/cat_<kategori>/`:

```json
{
  "id": "logic_05_custom_test",
  "title": "Custom Test Title",
  "category": "logic",
  "difficulty": "medium",
  "description": "Deskripsi singkat pengujian",
  "prompt": "Instruksi prompt yang dikirimkan ke LLM...",
  "evaluator_type": "python_unit_test",
  "test_code": "assert my_function(10) == 20\nprint('All tests passed!')"
}
```
