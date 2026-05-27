# AutoMate

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-0.4%2B-1C3C3C?logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/GPT--4o--mini-412991?logo=openai&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-D71F00?logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-45ba4b?logo=playwright&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Ready-000000?logo=vercel&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

<br/>

**Multi-agent business process automation platform** — AI-powered document intelligence pipeline that extracts structured data from identity documents, enriches it with government registry lookups, validates cross-references, and generates draft-filled legal documents.

> **Note:** This repository showcases the architecture, design patterns, and selected implementation examples. The full production implementation remains private.

<br/>

---

## Overview

AutoMate orchestrates a **LangGraph-based multi-agent pipeline** that transforms unstructured document inputs into structured, verified, and legally-drafted outputs. The system is designed for **human-in-the-loop verification**, graceful error recovery, and scalable cloud deployment.

### Pipeline Flow

```
Input (ID/Passport Image or JSON)
        │
        ▼
┌─────────────────┐
│   Extractor     │  ← GPT-4o-mini vision extraction
│   Agent         │     (image → structured person data)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Verification   │  ← Human-in-the-loop review
│     Gate        │     (interrupt/resume pattern)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Scraper       │  ← Government registry lookup
│   Agent         │     (multi-strategy: API → HTTP → Playwright)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ QA Inspector    │  ← Cross-reference validation
│   Agent         │     (business rule enforcement)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Scribe        │  ← DOCX template engine
│   Agent         │     (XML transform pipeline)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Final Review   │  ← Completeness verification
│   Agent         │
└─────────────────┘
```

---

## Key Features

| Feature | Description |
|---|---|
| **Vision-based Extraction** | GPT-4o-mini with structured output extraction from passport/ID images and PDFs |
| **Government Registry Scraping** | Multi-strategy company data lookup (API → HTTP → Playwright browser fallback) |
| **Human-in-the-Loop** | LangGraph interrupt/resume pattern for verification before proceeding |
| **QA Cross-Check Engine** | Business rule validation with automatic retry on failure |
| **DOCX Template Engine** | Clean XML transforms on OOXML templates — no PDF hacks, no unreliable text injection |
| **Multi-Person Support** | Full document sets for primary, partial sets for additional individuals |
| **Role-Based Contracts** | Per-person contract type selection (General, Kitchen, Cleaner) |
| **Async Background Processing** | Long-running extractions with polling/cancel support |
| **Cloud-Native Architecture** | Vercel-ready with serverless-compatible scraping fallbacks |

---

## Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** | Async REST API framework |
| **LangGraph** | Stateful multi-agent orchestration |
| **OpenAI GPT-4o-mini** | Vision extraction and text parsing |
| **SQLAlchemy 2.0** | Async ORM with SQLite/PostgreSQL |
| **Pydantic v2** | Strict runtime validation |
| **Playwright** | Browser automation fallback |
| **httpx** | Async HTTP client |

### Frontend
| Technology | Purpose |
|---|---|
| **Vanilla HTML/CSS/JS** | Lightweight, no-framework single-page application |
| **CSS Glassmorphism** | Modern dark-mode UI with backdrop blur effects |

### Infrastructure
| Technology | Purpose |
|---|---|
| **Vercel** | Serverless deployment |
| **Supabase** | PostgreSQL database (production) |
| **SQLite** | Local development database |

---

## Architecture

### Multi-Agent Graph

The core pipeline is built on **LangGraph's StateGraph** — each agent is a node that reads from and writes to a shared `ProcessState`:

```
START ──► Extractor ──► Verification Gate ──► Scraper ──► QA Inspector ──► Scribe ──► Final Review ──► END
   │                      │                      │             │
   └── (company-only)     └── (personal-only)    └── (retry)───┘
```

**State management** uses a TypedDict that flows through every node, enabling:
- Full traceability with per-agent audit logs
- Confidence scoring at each step
- Error accumulation without state corruption

### Document Generation Engine

The document engine uses **native OOXML manipulation** — it opens `.docx` files (which are ZIP archives containing XML), applies XPath-based paragraph transforms, and re-zippes the result. This preserves template formatting while injecting structured data from the extraction pipeline.

Key design decisions:
- **No PDF-to-text conversion** — works directly with structured XML
- **No unreliable regex injection** — uses proper XML namespace-aware transforms
- **Rich text support** — bold/normal segment injection within paragraphs
- **Missing field tracking** — every unresolved placeholder is collected and reported

### Scraping Strategy

The scraper uses a **degrading-fidelity fallback chain**:

1. **Deeds API** (internal JSON API) — fastest, no rendering needed
2. **HTTP GET + html-to-text** — works when JS rendering is unavailable
3. **CompanyBook API** — fallback for basic company metadata
4. **Playwright browser** — full JS rendering, local environments only

This ensures the system works in serverless environments (Vercel) while providing full fidelity when a browser is available.

---

## Design Patterns

| Pattern | Application |
|---|---|
| **State Graph** | LangGraph nodes with shared state for multi-agent orchestration |
| **Human-in-the-Loop** | Graph interruption at verification gate, resume via API |
| **Strategy Pattern** | Scraping fallback chain (API → HTTP → Playwright) |
| **Template Method** | Document transform pipeline with per-template overrides |
| **Chain of Responsibility** | Agent pipeline with conditional routing |
| **DTO Pattern** | Pydantic schemas for strict API contracts |
| **Repository Pattern** | Async SQLAlchemy session management |
| **Observer** | Frontend polling for background process status |

---

## Challenges Solved

### 1. Registry Scraping Reliability
**Challenge:** The target government registry is a JavaScript SPA that frequently changes layout and blocks automated access.

**Solution:** A multi-strategy fallback system that tries three approaches in order — internal API, plain HTTP, and Playwright browser — with abstract text parsing that normalizes the varied response formats into a consistent `CompanySchema`.

### 2. DOCX Template Filling Without Libraries
**Challenge:** Existing Python DOCX libraries couldn't handle the complex bilingual (Bulgarian/English) legal templates with mixed formatting.

**Solution:** Built a custom XML transformation engine that works directly on OOXML internals — parses paragraphs, detects context through normalized text matching, and injects formatted runs while preserving the original template styling.

### 3. Multi-Person Document Bundling
**Challenge:** Different people require different document sets (full for primary, partial for additional) with per-person contract type selection.

**Solution:** A flexible template selection system that maps contract types to template sets and automatically generates correct bundles per-person within a single API call.

### 4. Serverless Browser Automation
**Challenge:** Playwright cannot run in Vercel's serverless functions.

**Solution:** Separated scraping into a strategy pattern — serverless environments use API/HTTP strategies, while Playwright is reserved for local development, all abstracted behind a unified interface.

---

## Scalability Considerations

- **Async everywhere**: FastAPI async endpoints, async SQLAlchemy sessions, async LangGraph execution
- **Background processing**: Long-running extractions don't block the API
- **Multi-threaded document generation**: Each bundle generation is isolated and independently cacheable
- **Database-agnostic**: SQLite for development, PostgreSQL for production — switch via environment variable
- **Stateless graph execution**: LangGraph state persistence enables horizontal scaling with any checkpointer backend
- **Vercel edge-ready**: Serverless-compatible scraping with no hard infrastructure dependencies

---

## Security

- **No secrets in source** — all API keys and credentials are environment-injected
- **Input validation** — Pydantic v2 enforces strict type/format validation at every API boundary
- **No SQL injection** — async SQLAlchemy with parameterized queries throughout
- **Path traversal protection** — all file operations validate paths against allowed roots
- **CORS configured for development** — easily tightened for production deployments

---

## Showcase Structure

Since this is a structural showcase with the core production implementation remaining private, the repository is organized to highlight key architectural patterns rather than to be executed locally. 

You can explore the public-safe implementation examples in the `sample-code/` directory:

* **`state/`** → The unified `TypedDict` and Pydantic schemas flowing through the LangGraph pipeline.
* **`nodes/`** → Examples of individual agent node structures and error-handling wrappers.
* **`routing/`** → Conditional routing logic controlling the pipeline flow and human-in-the-loop gates.
* **`engine/`** → The custom OOXML/XPath XML transformation logic used for template generation.

---

## Sample Code

Selected public-safe code examples are available in the [`sample-code/`](./sample-code/) directory, demonstrating:

- [Shared Graph State Definition](./sample-code/process_state.py) — The TypedDict that flows through every agent
- [Pydantic Schemas](./sample-code/person_schema.py) — Strict validation contracts
- [LangGraph Node Pattern](./sample-code/extractor_agent.py) — How agents are structured
- [Conditional Routing](./sample-code/graph_routing.py) — How the graph branches
- [DOCX Transform Engine (Simplified)](./sample-code/docx_transform.py) — The XML templating approach
- [API Route Structure](./sample-code/api_routes.py) — Clean API design with FastAPI

---

## Lessons Learned

1. **Prefer deterministic parsing over LLM for structured data.** The hybrid approach — deterministic extraction for known formats, LLM enrichment for edge cases — proved far more reliable than relying on either alone.

2. **Graph orchestration beats sequential function calls.** LangGraph's interrupt/resume pattern made human-in-the-loop verification trivial compared to building custom state machines.

3. **OOXML is underrated as a template format.** Working directly with the XML inside `.docx` files gave precise control without the API limitations of high-level libraries.

4. **Fail fast, recover gracefully.** Each agent catches and records errors independently, allowing the system to fail one step without losing the entire process state.

---

## Future Improvements

- Self-hosted extraction model (vision transformer fine-tuned on passport layouts)
- Real-time WebSocket streaming for process status updates
- OCR-based document verification agent to replace the current stub
- Multi-language template support beyond Bulgarian/English
- Automated retraining pipeline for extraction accuracy improvements

---

## License

MIT

---

<p align="center">
  <i>Production implementation remains private while this repository showcases architecture, selected implementation examples, and technical decisions.</i>
</p>
