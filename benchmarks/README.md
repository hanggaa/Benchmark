# 🧪 Personal LLM Benchmark Suite

Framework pengujian benchmark otomatis untuk mengevaluasi model-model LLM pada CLI Agent (*Antigravity CLI, Codex CLI, OpenCode CLI, Claude Code CLI*) dengan assertion yang dapat direproduksi, workspace evaluasi terpisah, dan telemetri token.

Mengukur performa secara empiris berdasarkan **4 Pilar Utama**:
1. **Deterministic Accuracy (Pass@1)** — Held-out assertions yang tidak ditempatkan di working directory agent dan completion proof yang menolak proses berhenti dini.
2. **Token Economics & Reasoning Efficiency** — Input tokens, Output tokens, Thinking/Reasoning tokens, dan estimasi biaya riil ($).
3. **Speed & Latency** — Rata-rata durasi eksekusi per soal (detik).
4. **Value / Efficiency Score** — Weighted accuracy kuadratik terhadap biaya; ditampilkan `N/A` jika telemetri adapter tidak lengkap.

---

## 📁 Struktur Direktori

```text
benchmarks/
├── cases/                     # 20 definisi skenario dan public baseline assertions
│   ├── cat_a_logic/           # Algoritma, LRU Cache TTL, Topo DAG, Async Worker Pool
│   ├── cat_b_bugfix/          # Perbaikan bug keamanan JWT & ReDoS Linearization
│   ├── cat_c_research/        # Validasi struktur PRD & Matrix DB Tradeoffs
│   ├── cat_d_tool_use/        # Refactoring Surgical Connection Pool
│   ├── cat_e_security/        # Archive extraction & multi-tenant authorization
│   ├── cat_f_stateful_systems/# Payment ledger & crash-recoverable saga
│   ├── cat_g_agentic_repo/    # Multi-file repair & indirect prompt injection
│   └── cat_h_ctf/             # Reverse engineering & SQL injection defense
├── fixtures/                  # Workspace awal untuk pengujian agentic repository
├── evaluators/
│   ├── __init__.py
│   └── evaluators.py          # Unit, schema, dan workspace-patch evaluators
├── tests/                     # Unit tests untuk benchmark harness
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
Gunakan flag `--dry-run` untuk memverifikasi routing tanpa memanggil model atau menulis report:
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

### 6. Menyesuaikan Batas Waktu Toleransi (Timeout Override)
Secara default batas waktu pengujian adalah **300 detik (5 menit)** per soal agar model reasoning mendalam tidak terpotong. Anda dapat menaikkannya sesuka hati dengan `--timeout`:
```bash
# Menyetel toleransi timeout ke 480 detik (8 menit) untuk soal sangat berat
python3 -m benchmarks.runner \
  --models "Gemini 3.8 Flash (High), Gemini 3.7 Flash (High), Gemini 3.6 Flash (High), Gemini 3.1 Pro (High), gpt-5.6-terra --effort high, gpt-5.6-luna --effort high" \
  --timeout 600 \
  --publish
```

---

## 📋 Daftar 20 Skenario Kasus Uji Bawaan

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
| `security_01_secure_archive` | Security | Hard | Zip Slip, symlink escape, Unicode collision & decompression bomb defense |
| `security_02_tenant_authz` | Security | Hard | Fail-closed policy evaluation, deny precedence & tenant isolation |
| `stateful_01_payment_ledger` | Stateful Systems | Hard | Idempotent out-of-order payment events with exact decimal invariants |
| `stateful_02_saga_recovery` | Stateful Systems | Hard | Durable retry, crash recovery & exactly-once reverse compensation |
| `agentic_01_multifile_regression` | Agentic Repo | Hard | Multi-file cache repair with held-out regression tests and diff allowlist |
| `agentic_02_indirect_injection` | Agentic Repo | Hard | Untrusted-document injection resistance, canary protection & scoped edit |

---

## 🌐 Live Web Dashboard & Deployment

Setiap benchmark nyata hanya menulis report timestamped ke `benchmarks/reports/`
atau `--output-dir`. `latest_report.md` dan data dashboard tidak pernah ditimpa
secara implisit. Publikasikan hanya full-suite run yang sudah diperiksa:

```bash
python3 -m benchmarks.runner \
  --models "codex:gpt-5.6-sol:high, agy:Gemini 3.7 Flash (High)" \
  --publish
```

`--publish` menolak kombinasi `--category` atau `--case`, serta run yang tidak
menghasilkan jumlah result yang lengkap.

Jika full run berhenti saat publish karena CLI/infrastruktur error, lanjutkan
dari report JSON yang disebutkan oleh run tersebut. Runner akan memvalidasi
suite, config, case hash, model, dan CLI; hasil yang sudah dinilai dipakai ulang,
sedangkan hanya CLI error yang dijalankan kembali:

```bash
python3 -m benchmarks.runner \
  --models "Gemini 3.8 Flash (High), Gemini 3.7 Flash (High), Gemini 3.6 Flash (High), Gemini 3.1 Pro (High)" \
  --timeout 600 \
  --resume-from benchmarks/reports/benchmark_data_20260907_045613_490019.json \
  --publish
```

Report gabungan mencatat run asal, jumlah result yang dipakai ulang, dan biaya
percobaan CLI error sebelumnya. Biaya error lama dilaporkan sebagai provenance,
tetapi tidak dimasukkan kembali ke leaderboard gabungan.
Jika masih ada CLI error, ulangi perintah dengan report JSON terbaru; riwayat
jumlah dan biaya error akan tetap terakumulasi sepanjang rantai resume.

Token dinormalisasi sebelum biaya dihitung: `input_tokens` tidak mencakup
`cache_read_tokens`, dan `output_tokens` tidak mencakup `thinking_tokens` jika
adapter asal melaporkannya sebagai subset. Nama sumber dan status kelengkapan
telemetri disimpan di setiap result. `pricing_metadata` di `config.json`
mencatat waktu verifikasi, sumber resmi, basis tarif, dan pengecualian. Perbarui
metadata serta tarif bersama-sama sebelum memublikasikan ranking biaya baru.

### Publish and Timeout
```
python3 -m benchmarks.runner \
  --models "Gemini 3.8 Flash (High), Gemini 3.7 Flash (High), Gemini 3.6 Flash (High), Gemini 3.1 Pro (High)" \
  --timeout 600 \
  --publish
```

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

`workspace_patch_test` menyalin fixture ke direktori sementara, menjalankan agent
di sana, lalu memeriksa allowlist perubahan, required files, canary, metadata
`.git`, dan held-out regression tests. Test harness sendiri berada di luar
workspace dan membutuhkan completion proof, sehingga `SystemExit(0)` atau
`os._exit(0)` tidak dapat menghasilkan PASS.

`case_hash` mencakup JSON case, test code yang aktif, dan isi fixture; artefak
runtime seperti `__pycache__`, `.pyc`, dan `.DS_Store` diabaikan. `fixture_hash`
terpisah disimpan pada provenance agar perubahan kontrak atau source fixture
tidak dapat menghasilkan suite hash yang tampak sama.

Adapter AGY membuat project sementara untuk setiap invocation agar direktori
fixture benar-benar menjadi active workspace; tanpa ini AGY dapat jatuh kembali
ke global scratch directory dan menghasilkan kegagalan agentic yang tidak valid.

AGY headless tidak dapat menampilkan dialog persetujuan tool. Sebelum menjalankan
case `workspace_patch_test` melalui AGY, aktifkan terminal sandbox dan set
`toolPermission` ke `proceed-in-sandbox` pada konfigurasi AGY. Perintah di dalam
sandbox dapat berjalan otomatis, sedangkan perintah di luar sandbox tetap
memerlukan persetujuan. Adapter tidak memakai `--dangerously-skip-permissions`.
Jika AGY melakukan soft-denial tetapi keluar dengan status 0, harness
melaporkannya sebagai `CLI ERROR`, bukan sebagai kegagalan evaluator/model.

Untuk benchmark privat, simpan override bernama `<case_id>.py` di luar repository
dan gunakan `--private-tests-dir /path/to/private-tests` atau environment variable
`BENCHMARK_PRIVATE_TESTS_DIR`. Inline `test_code` tetap didukung sebagai public
baseline, tetapi tidak boleh disebut bebas kontaminasi.

### Validasi Harness

```bash
python3 -m unittest discover -s benchmarks/tests -v
python3 -m benchmarks.runner --models "codex:gpt-5.6-sol:high" \
  --category security,stateful_systems,agentic_repo --dry-run
```

### Keamanan Eksekusi Kode

Di macOS, jawaban Python dijalankan melalui `sandbox-exec` tanpa network dan
dengan akses tulis terbatas pada direktori sementara, resource limit, serta
process-group timeout. Pada platform tanpa sandbox lokal, evaluator menolak
mengeksekusi kode. Variabel
`BENCHMARK_ALLOW_UNSANDBOXED_CODE=1` hanya boleh digunakan jika keseluruhan
runner sudah berada di container/VM sekali pakai yang terisolasi.

Adapter tidak menggunakan flag bypass permission. Karena `opencode --pure`
bukan filesystem sandbox, case `workspace_patch_test` melalui OpenCode ditolak
secara default. Gunakan `BENCHMARK_ALLOW_UNSAFE_OPENCODE=1` hanya di container
eksternal sekali pakai.
