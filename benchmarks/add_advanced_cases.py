import json
from pathlib import Path

advanced_cases = [
    # 1. Async Worker Pool with Graceful Cancellation
    {
        "id": "logic_04_async_worker_pool",
        "title": "Async Worker Pool with Graceful Cancellation & Drain",
        "category": "logic",
        "difficulty": "hard",
        "description": "Implement an asynchronous worker pool supporting concurrency limits, priority scheduling, and graceful drain.",
        "prompt": """Write a complete Python implementation of an asynchronous worker pool class named `AsyncWorkerPool` using standard `asyncio`.

Requirements:
1. `__init__(self, concurrency: int = 3, max_queue_size: int = 100)`
2. `async def submit(self, coro_func, *args, priority: int = 0) -> asyncio.Future`:
   - Enqueues a coroutine function `coro_func(*args)` to be executed by the pool workers.
   - Higher priority integer executes before lower priority integers.
   - Returns an `asyncio.Future` that resolves with the result (or exception) of `coro_func(*args)`.
   - If pool is shutting down, raise `RuntimeError("Pool is shutting down")`.
3. `async def start(self) -> None`: Spawns worker tasks.
4. `async def shutdown(self, drain: bool = True, timeout: Optional[float] = 5.0) -> None`:
   - If `drain=True`, waits for all currently enqueued tasks to complete before stopping workers.
   - If `drain=False`, cancels all queued and currently executing tasks immediately.
   - Respects optional `timeout` seconds.
5. Must prevent deadlocks, handle task exceptions properly, and cancel tasks cleanly.

Provide only valid python code inside a ```python ``` block.""",
        "evaluator_type": "python_unit_test",
        "test_code": """
import asyncio

async def sample_task(val, delay=0.01):
    await asyncio.sleep(delay)
    return val * 2

async def error_task():
    await asyncio.sleep(0.01)
    raise ValueError("Task error occurred")

async def test_suite():
    pool = AsyncWorkerPool(concurrency=2)
    await pool.start()

    # Test 1: Standard task execution & results
    f1 = await pool.submit(sample_task, 10)
    f2 = await pool.submit(sample_task, 20)
    res1 = await f1
    res2 = await f2
    assert res1 == 20, f"Expected 20, got {res1}"
    assert res2 == 40, f"Expected 40, got {res2}"

    # Test 2: Exception propagation
    f_err = await pool.submit(error_task)
    try:
        await f_err
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Task error occurred" in str(e)

    # Test 3: Priority execution order
    execution_order = []
    async def ordered_task(tag):
        await asyncio.sleep(0.02)
        execution_order.append(tag)
        return tag

    # Fill worker slots first
    _ = await pool.submit(asyncio.sleep, 0.05)
    _ = await pool.submit(asyncio.sleep, 0.05)

    # Submit low and high priority while workers are busy
    f_low = await pool.submit(ordered_task, "LOW", priority=1)
    f_high = await pool.submit(ordered_task, "HIGH", priority=10)

    await asyncio.gather(f_low, f_high)
    assert execution_order == ["HIGH", "LOW"], f"Priority order mismatch: {execution_order}"

    # Test 4: Graceful shutdown with drain
    f_drain = await pool.submit(sample_task, 50, delay=0.02)
    await pool.shutdown(drain=True)
    assert await f_drain == 100

    # Test 5: Rejection after shutdown
    try:
        await pool.submit(sample_task, 1)
        assert False, "Should reject submit after shutdown"
    except RuntimeError:
        pass

    print("All AsyncWorkerPool tests passed successfully!")

asyncio.run(test_suite())
"""
    },

    # 2. ReDoS Security Vulnerability Patch
    {
        "id": "bugfix_02_redos_defense",
        "title": "Fix Catastrophic ReDoS Backtracking & Linearize Parser",
        "category": "bugfix",
        "difficulty": "hard",
        "description": "Fix exponential backtracking vulnerability in a regex validator so it executes in linear time.",
        "prompt": """Fix the security bug in the following markdown link and email parser function in Python:

```python
import re

# VULNERABILITY: Catastrophic backtracking on malicious unclosed strings
MARKDOWN_LINK_REGEX = re.compile(r'\[([a-zA-Z0-9_\s]+)+\]\((https?://[^\s)]+)\)')

def parse_markdown_links(text: str) -> list[dict[str, str]]:
    \"\"\"
    Extracts all markdown links [title](url) from text.
    Returns a list of dicts: [{"title": ..., "url": ...}].
    Must be safe against ReDoS attacks (linear time complexity).
    \"\"\"
    results = []
    for match in MARKDOWN_LINK_REGEX.finditer(text):
        results.append({"title": match.group(1), "url": match.group(2)})
    return results
```

Requirements:
1. Fix the regex or parsing logic so it NEVER exhibits polynomial or exponential backtracking ($O(N)$ execution time).
2. Correctly extract valid markdown links formatted as `[Link Title](https://example.com)`.
3. Support titles with letters, numbers, spaces, and underscores.
4. If an evil input containing 50,000 unclosed brackets `[` or unclosed titles is passed, it must execute in less than 0.05 seconds without hanging.

Provide the complete fixed function inside a ```python ``` block.""",
        "evaluator_type": "python_unit_test",
        "test_code": """
import time

# Test 1: Valid markdown links extraction
sample_text = "Check out [Google Search](https://google.com) and [GitHub Repo 2026](https://github.com/test)."
links = parse_markdown_links(sample_text)
assert len(links) == 2, f"Expected 2 links, got {len(links)}"
assert links[0]["title"] == "Google Search"
assert links[0]["url"] == "https://google.com"
assert links[1]["title"] == "GitHub Repo 2026"
assert links[1]["url"] == "https://github.com/test"

# Test 2: ReDoS Attack Payload (evil unclosed brackets & nested spaces)
evil_payload = "[" + "a" * 30000 + "!"
start_time = time.perf_counter()
res = parse_markdown_links(evil_payload)
elapsed = time.perf_counter() - start_time

assert len(res) == 0
assert elapsed < 0.1, f"ReDoS defense failed! Took {elapsed:.3f}s (must be < 0.1s)"

# Test 3: Multiple unclosed brackets payload
evil_payload_2 = ("[" * 5000) + ("a " * 5000) + "!"
start_time = time.perf_counter()
res2 = parse_markdown_links(evil_payload_2)
elapsed2 = time.perf_counter() - start_time

assert elapsed2 < 0.1, f"ReDoS defense failed on nested spaces! Took {elapsed2:.3f}s"

print("All ReDoS Defense tests passed successfully!")
"""
    }
]

for case in advanced_cases:
    cat = case["category"]
    if cat == "logic":
        path = Path("benchmarks/cases/cat_a_logic") / f"{case['id']}.json"
    elif cat == "bugfix":
        path = Path("benchmarks/cases/cat_b_bugfix") / f"{case['id']}.json"
    elif cat == "research":
        path = Path("benchmarks/cases/cat_c_research") / f"{case['id']}.json"
    else:
        path = Path("benchmarks/cases/cat_d_tool_use") / f"{case['id']}.json"

    path.write_text(json.dumps(case, indent=2), encoding="utf-8")
    print(f"Added advanced case: {path}")
