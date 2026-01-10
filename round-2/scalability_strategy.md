# CODE-Sherpa — Scalability Strategy (Round 2 Architecture)

> **Authority Notice**
> This document defines the scalability protocols for the Round 2 "Hybrid Graph-RAG" architecture.
> It details how the system handles high concurrency and large repositories using the new Sherpa Brain layer.

---

## 1. The Core Challenge: Scaling Hybrid Intelligence
Scaling a purely static analyzer is simple (just run it). Scaling a **Hybrid AI System** is difficult because:
1.  **LLM Costs:** Analyzing every function with AI is prohibitively expensive.
2.  **Latency:** AI generation is slow compared to AST parsing.
3.  **Context Limits:** Large repositories (monorepos) exceed standard token windows.

CODE-Sherpa solves these via a **"Structure-First, AI-Second"** strategy.

---

## 2. Theoretical Cloud Architecture (The "10k Users" Plan)

To handle 10,000 concurrent users without crashing or bankrupting the project, we propose the following 3-tier strategy:

### 2.1 Tier 1: Semantic Caching (The Redis Layer)
We utilize a content-addressable cache to prevent redundant AI computation.
* **Mechanism:** Before sending code to the *Sherpa Brain*, we generate a SHA-256 hash of the function's AST node.
* **Logic:**
    * `IF hash exists in Redis` → Return cached explanation (Latency: <5ms).
    * `IF hash is new` → Send to LLM → Cache the result.
* **Impact:** For popular open-source libraries (e.g., React, Pandas), cache hit rates are expected to exceed **85%**, reducing AI costs to near zero.

### 2.2 Tier 2: AST-Based Pruning (Token Optimization)
We do not send raw files to the AI. The *Static Analyzer* acts as a filter.
* **The Filter:** We strip comments, blank lines, and untyped variables before the AI sees the code.
* **The "Skeleton" Prompt:** We send only the *signature* and *logic flow* to the AI, not the boilerplate.
* **Impact:** Reduces token usage by ~40% per request, allowing for faster response times.

### 2.3 Tier 3: Asynchronous "Just-in-Time" Analysis
For massive repositories, we do not analyze everything upfront.
1.  **Phase 1 (Immediate):** Parse Entry Points and Depth-1 dependencies. (User sees results in seconds).
2.  **Phase 2 (Background):** A task queue (Celery/RabbitMQ) processes deeper files while the user is reading the Phase 1 tour.
3.  **Phase 3 (On-Demand):** If a user clicks a deep module, we trigger a high-priority analysis job instantly.

---

## 3. Reliability & Failure Modes

Static analysis inevitably encounters edge cases. CODE-Sherpa handles them explicitly to ensure robust scaling.

### 3.1 Syntax Errors & partial Parsing
* **Problem:** A repository contains invalid Python syntax (e.g., a file meant for Python 2 run in a Python 3 environment).
* **Handling:** The AST parser wraps file operations in strict `try-except` blocks.
* **Result:** The system logs the error, marks the specific file as "Unparseable," and continues analyzing the rest of the repository. The tour explicitly warns the user about the missing context.

### 3.2 Circular Dependencies
* **Problem:** File A imports B, which imports A. Naive recursion would crash the stack.
* **Handling:** The graph builder maintains a `visited` set during traversal.
* **Result:** Cycles are detected and "broken" visually in the flowchart (marked with a dashed line), preventing infinite loops.

### 3.3 Dynamic or Unresolvable Constructs
* **Problem:** Python code using `importlib` or dynamic `eval()` cannot be statically determined.
* **Handling:** The system operates on a "Best Effort" basis. It reports only what is statically visible.
* **Result:** Missing information is left unresolved rather than guessed (Zero Hallucination Policy).

---

## 4. Architectural Limits (Explicit)

To maintain determinism and protect resources, we enforce the following hard limits:

### 4.1 File Size Cap
* **Limit:** Files > 10,000 lines.
* **Behavior:** Treated as "Black Boxes." The system extracts the filename but skips detailed function parsing and AI summarization.

### 4.2 Recursion Depth
* **Limit:** Analysis halts at depth 20.
* **Reason:** Prevents infinite loops in complex spaghetti code.

### 4.3 Analysis Timeout
* **Limit:** 30 seconds per "Phase 1" scan.
* **Behavior:** If analysis exceeds this time, the system returns the partial graph built so far and queues the rest for background processing.

---

## 5. Summary of Scalability
CODE-Sherpa scales because it is **lazy by default**. It calculates structure locally (cheap) and invokes intelligence remotely (expensive) only when necessary and unique.

This architecture moves from a "Script" (Round 1) to a "Platform" (Round 2) capable of handling enterprise-grade loads.