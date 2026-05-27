# Technical Decisions

> Key architectural decisions, trade-offs, and rationale behind the design choices.

---

## 1. LangGraph Over Custom State Machine

**Decision:** Use LangGraph's StateGraph for pipeline orchestration.

**Alternatives considered:**
- Custom Python state machine (if/elif chains)
- Prefect / Airflow DAGs
- Simple function composition with callbacks

**Rationale:**
- LangGraph provides **built-in interrupt/resume** for human-in-the-loop — something that would require significant custom infrastructure otherwise
- The **TypedDict-based state** gives type safety without the overhead of a full framework
- **Checkpointing** (memory saver) comes free and enables process cancellation
- The graph visualization is self-documenting — the route functions double as documentation

**Trade-off:** Adds a dependency that's less mature than alternatives. Mitigated by keeping agent nodes as simple async functions that only read/write state — making them testable independently.

---

## 2. Native OOXML Over Python-DOCX Libraries

**Decision:** Manipulate `.docx` files directly at the XML level via ElementTree.

**Alternatives considered:**
- `python-docx` (python-pptx's sibling)
- `docxtpl` (Jinja2 for DOCX)
- LibreOffice macro automation

**Rationale:**
- The templates contain **complex bilingual layouts** with mixed bold/normal text, right-aligned signature blocks, and nested tables — none of the existing libraries could handle all cases
- OOXML is just a **ZIP of XML files** — the transform pipeline is straightforward with proper namespace handling
- **Deterministic output** — no dependency on external office software
- **Fine-grained control** — can inject rich text segments, adjust tab stops, merge rows, etc.

**Trade-off:** More code to write and maintain than using a library. Mitigated by keeping transforms composable — each document type gets its own transformation function, and shared helpers (paragraph text, run injection) are reused.

---

## 3. Hybrid Parsing: Deterministic + LLM

**Decision:** Use deterministic (regex/heuristic) parsing as the primary extraction method for registry data, with LLM enrichment only as fallback.

**Alternatives considered:**
- Pure LLM extraction for everything
- Pure deterministic parsing
- ML model fine-tuned on registry data

**Rationale:**
- Registry data follows **predictable numbered-section layout** — regex extraction is faster, cheaper, and more reliable than calling an LLM
- LLM extraction occasionally **hallucinates** fields or misinterprets structured data
- The hybrid approach uses LLM **only when deterministic parsing fails** (corrupted text, unexpected format)
- Result: ~95% of cases handled by fast deterministic parsing, ~5% fall back to LLM

**Trade-off:** Two code paths to maintain. Mitigated by the LLM fallback being a simple prompt call wrapped in try/except.

---

## 4. Multi-Strategy Scraping Over Single Approach

**Decision:** Implement a fallback chain of scraping strategies.

```
Deeds API (JSON) → HTTP GET → CompanyBook API → Playwright Browser
```

**Alternatives considered:**
- Always use Playwright
- Always use HTTP + html-to-text
- Use a third-party API service

**Rationale:**
- Playwright **cannot run in serverless environments** (Vercel)
- The Deeds API is **fast and reliable** when available
- Each fallback adds **fidelity at the cost of speed**
- The chain ensures the system works **everywhere**, from edge functions to local dev

**Trade-off:** More code. Mitigated by the unified return interface — each strategy returns the same `{raw_text, source, company_hint}` shape.

---

## 5. Background Tasks Over WebSockets

**Decision:** Run extractions as `asyncio.create_task` with HTTP polling, not WebSockets.

**Alternatives considered:**
- WebSocket streaming for real-time updates
- Server-Sent Events (SSE)
- Pure synchronous request/response

**Rationale:**
- Extraction takes 3–15 seconds — fast enough that polling every 2 seconds is responsive
- **Simpler deployment** — no WebSocket infrastructure needed
- Works with **serverless** (Vercel) where persistent connections are problematic
- The polling endpoint restores full state from the database, so **interruptions are recoverable**

**Trade-off:** Slightly higher latency on status updates vs WebSocket. Acceptable for the use case.

---

## 6. In-Memory State for Frontend

**Decision:** Store workflow session state in JavaScript memory, not localStorage/sessionStorage.

**Alternatives considered:**
- IndexedDB
- localStorage
- Server-side session state

**Rationale:**
- The app is a **single-page application** where users complete their workflow in one session
- **No persistence needed** — refreshing the page starts fresh (which is the desired UX)
- Keeps the frontend **dependency-free** — no storage abstraction library needed
- The data flows are simple: extract → edit → generate documents. No multi-step wizards that span sessions.

**Trade-off:** Data is lost on page refresh. Acceptable for an MVP/portfolio piece.

---

## 7. SQLite for Development, PostgreSQL for Production

**Decision:** Support both via environment variable switching.

**Alternatives considered:**
- Always use PostgreSQL (heavy for local dev)
- Always use SQLite (different behavior than production)

**Rationale:**
- SQLite is **zero-config** for local development
- Async SQLAlchemy abstracts the differences well
- `pool_pre_ping` flag handles PostgreSQL connection staleness transparently
- The `postgres://` to `postgresql+asyncpg://` auto-conversion removes an annoying config step

**Trade-off:** Must test with PostgreSQL before deploying. Mitigated by CI pipeline.

---

## 8. Pydantic v2 With StrictStr

**Decision:** Use `StrictStr` on all schema string fields.

**Alternatives considered:**
- Python `str` type
- Pydantic v1 `constr()`
- Custom validators

**Rationale:**
- `StrictStr` prevents **silent coercion** of non-string types (e.g., integers passed as names)
- Provides **clear error messages** on type mismatch
- Pydantic v2 is ~5-10x faster than v1 for validation
- The `@field_validator` pattern allows complex cross-field validation alongside simple type checks

**Trade-off:** More verbose schema definitions. Mitigated by the clarity of errors during development.
