# 🏆 Personal LLM Benchmark Leaderboard

> Benchmark execution completed for **1** model configuration(s) across **2** total runs.

## 📊 Overall Model Comparison

| Model | CLI | Effort | Pass Rate | Avg Latency | Thinking Tokens | Total Cost ($) | Efficiency Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.7 Flash (High)** | `agy` | `-` | **50.0%** (1/2) | 18.22s | 6,082 | $0.09535 | **498** |

## 📂 Category Breakdown (Pass Rates)

| Model | CLI | Effort | Bugfix | Logic |
| :--- | :--- | :--- | :---: | :---: |
| **Gemini 3.7 Flash (High)** | `agy` | `default` | 100% (1/1) | 0% (0/1) |

## 📝 Detailed Test Execution Logs

### ❌ FAIL: Async Worker Pool with Graceful Cancellation & Drain (`logic_04_async_worker_pool`)
- **Model**: `Gemini 3.7 Flash (High)` via `agy`
- **Duration**: 20.53s
- **Tokens**: In: 17,988 | Out: 5,868 | Thinking: 4,529 | Cost: $0.04918
- **Error Details**:
```
Test failure (exit code 1):
Traceback (most recent call last):
  File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmppntzdwce.py", line 219, in <module>
    asyncio.run(test_suite())
    ~~~~~~~~~~~^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 725, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/var/folders/w2/d2b442v115n56_9c4ggy80l9h9m9ch/T/tmppntzdwce.py", line 206, in test_suite
    f_drain = await pool.submit(sample_task, 50, delay=0.02)
                    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: AsyncWorkerPool.submit() got an unexpected keyword argument 'delay'
```

### ✅ PASS: Fix Catastrophic ReDoS Backtracking & Linearize Parser (`bugfix_02_redos_defense`)
- **Model**: `Gemini 3.7 Flash (High)` via `agy`
- **Duration**: 15.92s
- **Tokens**: In: 25,510 | Out: 2,619 | Thinking: 1,553 | Cost: $0.04617
