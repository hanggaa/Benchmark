import json
from pathlib import Path

cases = [
    # Category A: Logic & Algorithmic
    {
        "id": "logic_01_lru_ttl",
        "title": "Thread-Safe LRU Cache with TTL & Eviction",
        "category": "logic",
        "difficulty": "hard",
        "description": "Implement a thread-safe LRU Cache with TTL expiration and cleanup.",
        "prompt": """Write a complete Python implementation of a thread-safe LRU cache class named `TimeBoundedLRUCache`.
Requirements:
1. `__init__(self, capacity: int, default_ttl_seconds: float = 60.0)`
2. `set(self, key: str, value: any, ttl: Optional[float] = None) -> None`: Inserts or updates key. If capacity is reached, evict the least recently used NON-EXPIRED item (or oldest expired item).
3. `get(self, key: str) -> Optional[any]`: Returns value if present and not expired, else None. Accessing updates LRU recency.
4. `delete(self, key: str) -> bool`: Deletes key, returns True if existed and deleted, else False.
5. `cleanup_expired() -> int`: Removes all expired keys and returns count of removed items.
6. `size() -> int`: Returns number of currently valid (non-expired) items.
7. Must be thread-safe using `threading.RLock`.

Provide only valid python code inside a ```python ``` block.""",
        "evaluator_type": "python_unit_test",
        "test_code": """
import time
import threading

cache = TimeBoundedLRUCache(capacity=3, default_ttl_seconds=1.0)
cache.set("a", 100)
cache.set("b", 200)
cache.set("c", 300)

assert cache.get("a") == 100, "Get failed for key 'a'"
assert cache.get("b") == 200, "Get failed for key 'b'"

# Eviction test: adding 'd' should evict 'c' since 'a' and 'b' were accessed
cache.set("d", 400)
assert cache.get("c") is None, "Key 'c' should have been evicted"
assert cache.get("d") == 400, "Key 'd' should exist"
assert cache.size() == 3, f"Expected size 3, got {cache.size()}"

# TTL Expiration test
cache.set("temp", 999, ttl=0.1)
assert cache.get("temp") == 999
time.sleep(0.15)
assert cache.get("temp") is None, "Key 'temp' should be expired"

# Cleanup test
cache.set("exp1", 1, ttl=0.05)
cache.set("exp2", 2, ttl=0.05)
time.sleep(0.08)
removed = cache.cleanup_expired()
assert removed >= 2, f"Expected at least 2 cleaned up, got {removed}"

# Thread safety concurrency test
threads = []
def worker(w_id):
    for i in range(50):
        cache.set(f"k_{w_id}_{i}", i, ttl=1.0)
        _ = cache.get(f"k_{w_id}_{i}")

for tid in range(5):
    t = threading.Thread(target=worker, args=(tid,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All LRU TTL tests passed!")
"""
    },
    {
        "id": "logic_02_topo_cycle",
        "title": "Topological Batch Scheduler with Cycle Detection",
        "category": "logic",
        "difficulty": "medium",
        "description": "Compute parallel execution stages for a DAG or detect circular dependency paths.",
        "prompt": """Implement a Python class `DependencyResolver` with custom exception `CircularDependencyError(Exception)`:
Requirements:
1. Method `resolve(dependencies: dict[str, list[str]]) -> list[list[str]]`
   - `dependencies` maps task_name -> list of task_names it DEPENDS ON (must run before it).
   - Returns a list of stages (batches). Each stage is a sorted list of task names that can run in parallel.
   - If any circular dependency exists (e.g. A->B->A or self-loop A->A), raise `CircularDependencyError`.
2. Tasks with no dependencies execute in stage 0.

Provide only valid python code inside a ```python ``` block.""",
        "evaluator_type": "python_unit_test",
        "test_code": """
resolver = DependencyResolver()

# Test 1: Simple DAG
deps1 = {
    "build": [],
    "lint": [],
    "test": ["build", "lint"],
    "package": ["test"],
    "deploy": ["package"]
}
stages = resolver.resolve(deps1)
assert stages[0] == ["build", "lint"], f"Stage 0 failed: {stages[0]}"
assert stages[1] == ["test"], f"Stage 1 failed: {stages[1]}"
assert stages[2] == ["package"], f"Stage 2 failed: {stages[2]}"
assert stages[3] == ["deploy"], f"Stage 3 failed: {stages[3]}"

# Test 2: Cycle detection
deps_cycle = {
    "A": ["B"],
    "B": ["C"],
    "C": ["A"]
}
try:
    resolver.resolve(deps_cycle)
    assert False, "Should have raised CircularDependencyError"
except CircularDependencyError:
    pass

# Test 3: Self-loop
deps_self = {"A": ["A"]}
try:
    resolver.resolve(deps_self)
    assert False, "Should have raised CircularDependencyError for self loop"
except CircularDependencyError:
    pass

print("All Topo Cycle tests passed!")
"""
    },
    {
        "id": "logic_03_sliding_rate_limiter",
        "title": "Sliding Window Log Rate Limiter",
        "category": "logic",
        "difficulty": "medium",
        "description": "Implement precise sliding window rate limiting with retry-after calculation.",
        "prompt": """Implement a thread-safe Python class `SlidingWindowRateLimiter`:
Requirements:
1. `__init__(self, max_requests: int, window_seconds: float)`
2. `allow_request(self, key: str, timestamp: Optional[float] = None) -> tuple[bool, float]`:
   - Returns `(is_allowed: bool, retry_after_seconds: float)`.
   - If allowed: returns `(True, 0.0)`.
   - If rate limited: returns `(False, retry_after)`. `retry_after` is how many seconds until at least 1 request slot frees up.
3. `get_remaining(self, key: str, timestamp: Optional[float] = None) -> int`: Returns remaining requests available in current sliding window.

Provide only valid python code inside a ```python ``` block.""",
        "evaluator_type": "python_unit_test",
        "test_code": """
limiter = SlidingWindowRateLimiter(max_requests=2, window_seconds=10.0)

t0 = 1000.0
# Request 1 at t0
allowed, retry = limiter.allow_request("user1", timestamp=t0)
assert allowed is True and retry == 0.0
assert limiter.get_remaining("user1", timestamp=t0) == 1

# Request 2 at t0 + 2
allowed, retry = limiter.allow_request("user1", timestamp=t0 + 2.0)
assert allowed is True and retry == 0.0
assert limiter.get_remaining("user1", timestamp=t0 + 2.0) == 0

# Request 3 at t0 + 5 (should be rejected)
allowed, retry = limiter.allow_request("user1", timestamp=t0 + 5.0)
assert allowed is False
# First request was at 1000.0, so slot opens at 1010.0. Current is 1005.0 -> retry = 5.0
assert abs(retry - 5.0) < 0.01, f"Expected retry ~5.0, got {retry}"

# Request 4 at t0 + 11 (first request expired)
allowed, retry = limiter.allow_request("user1", timestamp=t0 + 11.0)
assert allowed is True

print("All Rate Limiter tests passed!")
"""
    },

    # Category B: Bug Fix
    {
        "id": "bugfix_01_jwt_verifier",
        "title": "Fix JWT Verification Security Vulnerabilities",
        "category": "bugfix",
        "difficulty": "medium",
        "description": "Fix token expiration boundary condition and 'none' alg vulnerability.",
        "prompt": """Fix the security bugs in the following JWT verifier function in Python:

```python
import base64
import json
import hmac
import hashlib
import time

def verify_jwt(token: str, secret_key: str, allowed_algs: list[str] = ["HS256"]) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")
    
    header_raw = base64.urlsafe_b64decode(parts[0] + "==")
    header = json.loads(header_raw)
    
    payload_raw = base64.urlsafe_b64decode(parts[1] + "==")
    payload = json.loads(payload_raw)
    
    # BUG 1: Does not validate header algorithm against allowed_algs properly
    alg = header.get("alg")
    if alg == "none":
        return payload
        
    # BUG 2: Expiration logic fails on exact timestamp or missing exp
    now = time.time()
    if "exp" in payload and payload["exp"] < now:
        raise ValueError("Token expired")
        
    # Verify HMAC signature
    signature = base64.urlsafe_b64decode(parts[2] + "==")
    signing_input = f"{parts[0]}.{parts[1]}".encode("utf-8")
    expected_sig = hmac.new(secret_key.encode("utf-8"), signing_input, hashlib.sha256).digest()
    
    if not hmac.compare_digest(signature, expected_sig):
        raise ValueError("Invalid signature")
        
    return payload
```

Requirements:
- Ensure `alg` MUST strictly be in `allowed_algs` (reject "none" or unapproved algorithms).
- If `exp` is present and `exp <= now`, raise `ValueError("Token expired")`.
- Handle proper Base64 URL decoding with dynamic padding.
- Return the decoded payload dictionary if valid.

Provide the complete fixed function inside a ```python ``` block.""",
        "evaluator_type": "python_unit_test",
        "test_code": """
import base64
import json
import hmac
import hashlib
import time

secret = "my-super-secret-key-12345"

def make_token(header, payload, secret_key):
    def b64(d):
        return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    h_b64 = b64(header)
    p_b64 = b64(payload)
    sig = base64.urlsafe_b64encode(
        hmac.new(secret_key.encode(), f"{h_b64}.{p_b64}".encode(), hashlib.sha256).digest()
    ).decode().rstrip("=")
    return f"{h_b64}.{p_b64}.{sig}"

# Test 1: Valid token
tok1 = make_token({"alg": "HS256", "typ": "JWT"}, {"sub": "alice", "exp": time.time() + 100}, secret)
res = verify_jwt(tok1, secret, ["HS256"])
assert res["sub"] == "alice"

# Test 2: Expired token
tok_exp = make_token({"alg": "HS256"}, {"sub": "bob", "exp": time.time() - 1}, secret)
try:
    verify_jwt(tok_exp, secret, ["HS256"])
    assert False, "Should have rejected expired token"
except ValueError:
    pass

# Test 3: 'none' alg attack
def b64_raw(d):
    return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
tok_none = f"{b64_raw({'alg': 'none'})}.{b64_raw({'sub': 'attacker'})}."
try:
    verify_jwt(tok_none, secret, ["HS256"])
    assert False, "Should have rejected 'none' alg token"
except (ValueError, Exception):
    pass

# Test 4: Tampered signature
tok_tampered = tok1[:-4] + "abcd"
try:
    verify_jwt(tok_tampered, secret, ["HS256"])
    assert False, "Should have rejected invalid signature"
except ValueError:
    pass

print("All JWT Verifier tests passed!")
"""
    },

    # Category C: Deep Research & Schema Adherence
    {
        "id": "research_01_prd_structure",
        "title": "PRD Generation with Strict Handoff Context",
        "category": "research",
        "difficulty": "medium",
        "description": "Generate a structured PRD document following precise section headers and machine-readable handoff context.",
        "prompt": """Generate a structured Product Requirement Document (PRD) for an AI developer tool called "QueryLens" (an AI SQL query optimizer and visual explainer).

You MUST organize your response strictly using the following Markdown sections:
# PRD: QueryLens MVP
## Project Overview & Core Concept
## Target Persona & Key Pain Points
## Core Functional Requirements (MVP)
## Out of Scope (Not in MVP)
## Tech Stack & Architecture Decisions
## Handoff Context

Under `## Handoff Context`, provide exact key-value pairs formatted as:
- Stage: prd
- App name: QueryLens
- User level: B
- Target platform: web
- Budget: under $100/month
- Timeline: 4 weeks

Do not omit any required section.""",
        "evaluator_type": "schema_check",
        "expected_structure": {
            "required_headings": [
                "Project Overview & Core Concept",
                "Target Persona & Key Pain Points",
                "Core Functional Requirements (MVP)",
                "Out of Scope (Not in MVP)",
                "Tech Stack & Architecture Decisions",
                "Handoff Context"
            ],
            "required_substrings": [
                "QueryLens",
                "Stage: prd",
                "App name: QueryLens",
                "User level: B",
                "Target platform: web"
            ]
        }
    },
    {
        "id": "research_02_database_tradeoff",
        "title": "Vector Database Tradeoff & Pricing Comparison Matrix",
        "category": "research",
        "difficulty": "medium",
        "description": "Produce a comparative matrix between pgvector, Qdrant, and Pinecone with cost projections.",
        "prompt": """Provide a comprehensive technical comparison for vector search engines supporting a 10-million vector workload (1536 dimensions): pgvector (PostgreSQL), Qdrant, and Pinecone.

You MUST include:
1. A Markdown table with EXACT columns: `| Engine | Architecture Type | Estimated Monthly Cost | Latency p95 | Key Pros | Key Cons |`
2. Rows for `pgvector`, `Qdrant`, and `Pinecone`.
3. Specific dollar estimates ($) in the cost column.
4. A concluding section with heading `## Recommendation Matrix`.
""",
        "evaluator_type": "schema_check",
        "expected_structure": {
            "required_headings": [
                "Recommendation Matrix"
            ],
            "required_substrings": [
                "| Engine |",
                "pgvector",
                "Qdrant",
                "Pinecone",
                "$"
            ]
        }
    },

    # Category D: Tool Use & Clean Refactoring
    {
        "id": "tool_01_surgical_refactor",
        "title": "Surgical Connection Pool with Auto-Reconnection",
        "category": "tool_use",
        "difficulty": "medium",
        "description": "Extend connection pool with healthcheck while preserving existing signatures.",
        "prompt": """Implement a robust database connection pool wrapper in Python named `ResilientConnectionPool`.
Requirements:
1. `__init__(self, max_connections: int = 5, ping_timeout: float = 1.0)`
2. `acquire() -> dict`: Returns an active connection object `{"id": int, "alive": bool}`. If no available connections, raise `RuntimeError("Pool exhausted")`.
3. `release(conn: dict) -> None`: Returns connection back to the pool.
4. `health_check_and_heal() -> int`: Iterates over pool connections, checks if `conn["alive"]` is False, recreates them with new alive connections, and returns the number of healed connections.
5. `close_all() -> None`: Closes and empties the pool.

Provide only valid python code inside a ```python ``` block.""",
        "evaluator_type": "python_unit_test",
        "test_code": """
pool = ResilientConnectionPool(max_connections=3)

c1 = pool.acquire()
c2 = pool.acquire()
c3 = pool.acquire()

assert c1["alive"] is True
assert c2["alive"] is True
assert c3["alive"] is True

try:
    pool.acquire()
    assert False, "Should raise RuntimeError on exhausted pool"
except RuntimeError:
    pass

# Simulate connection failure on c1
c1["alive"] = False
pool.release(c1)
pool.release(c2)
pool.release(c3)

healed_count = pool.health_check_and_heal()
assert healed_count == 1, f"Expected 1 healed connection, got {healed_count}"

# Acquire again to verify new alive connection
c_new = pool.acquire()
assert c_new["alive"] is True

pool.close_all()
print("All Resilient Pool tests passed!")
"""
    }
]

for case in cases:
    cat = case["category"]
    filename = f"cat_{cat[:1]}_{case['id']}.json"
    if cat == "logic":
        path = Path("benchmarks/cases/cat_a_logic") / f"{case['id']}.json"
    elif cat == "bugfix":
        path = Path("benchmarks/cases/cat_b_bugfix") / f"{case['id']}.json"
    elif cat == "research":
        path = Path("benchmarks/cases/cat_c_research") / f"{case['id']}.json"
    else:
        path = Path("benchmarks/cases/cat_d_tool_use") / f"{case['id']}.json"

    path.write_text(json.dumps(case, indent=2), encoding="utf-8")
    print(f"Created case: {path}")
