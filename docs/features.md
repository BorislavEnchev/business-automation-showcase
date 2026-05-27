# Features

> Comprehensive breakdown of AutoMate's capabilities, organized by subsystem.

---

## 1. Multi-Agent Pipeline

### Vision-Based Document Extraction
- Accepts passport/ID images or PDF files via base64 upload
- Uses **GPT-4o-mini** with structured JSON output extraction
- Supports both Cyrillic and Latin text on same document
- Normalizes dates, names, and identifiers into strict schema
- Falls back gracefully on missing or illegible fields
- Handles multi-page PDF documents (converts to images internally)

### Manual JSON Input
- Direct JSON input for testing and manual data entry
- Legacy format normalization (accepts `full_name`, converts to structured fields)
- Same Pydantic validation as image extraction path

### Human-in-the-Loop Verification
- LangGraph `interrupt()` pauses execution after extraction
- User reviews extracted data via API or frontend
- User can approve, reject, or submit corrections
- Corrected data flows forward to subsequent pipeline steps
- Personal-only mode skips verification if data is pre-approved

---

## 2. Company Registry Scraping

### Multi-Strategy Data Retrieval

The scraper employs a **degrading-fidelity fallback chain**:

| Priority | Strategy | Environment | Speed | Fidelity |
|---|---|---|---|---|
| 1 | Internal Deeds API (JSON) | All | Fast | High |
| 2 | HTTP GET + html-to-text | All | Medium | Medium |
| 3 | CompanyBook API | All | Medium | Basic |
| 4 | Playwright Browser | Local only | Slow | Full |

### Deterministic Parsing Pipeline
- Case reference normalization
- Mojibake (encoding corruption) repair for Bulgarian Cyrillic
- Section-based field extraction from numbered registry forms
- Regex-based phone, email, and address extraction
- Legal form abbreviation detection and normalization
- LLM enrichment for edge cases and corrupted data

### Extracted Data Schema
Structured `CompanySchema` output:
- **Identifiers**: Company name, EIK/BULSTAT number, legal form
- **Addresses**: Registered office, management address, full formatted address
- **Management**: Manager full name, EGN, representative role
- **Contact**: Contact person, phone, email

---

## 3. QA Cross-Check Engine

### Validation Rules
- Person data must be present
- Company data must be present
- Company core identifiers (name, number, legal form) are required
- Optional: person/manager name alignment check (soft warning)

### Retry Logic
- Configurable max retries (default: 3)
- Failed validation triggers automatic re-scraping
- Permanent failure after max retries exhausted
- Full audit trail with per-attempt logging

---

## 4. DOCX Document Generation Engine

### Template System
- Native OOXML (`.docx`) templates — ZIP archives containing XML
- Per-template transformation functions with context-aware text replacement
- Rich text injection (bold/normal segments within same paragraph)
- Layout fixes for specific document types (declarations, contracts)

### Supported Document Types

| Document | Features |
|---|---|
| **Service Agreement** | Date/city injection, client details, contact info, address |
| **Employment Contract (General)** | Bilingual (EN/BG), table-based layout, AND/И name row merging |
| **Employment Contract (Kitchen)** | Same engine, different contract-specific boilerplate |
| **Employment Contract (Cleaner)** | Same engine, different contract-specific boilerplate |
| **Condition Declaration** | Manager details, bilingual declarator name, rich text formatting |
| **Foreigners Declaration** | Right-aligned declarator, tab-stop positioning for signature |
| **Motivation Letter** | Company description, activity, date, signature block |
| **Power of Attorney** | Manager identification, company details, representation scope |

### Missing Field Tracking
Every unresolved placeholder is:
1. Replaced with a clear `[LIPSVA: field_name]` marker
2. Collected into the document's `missing_fields` list
3. Aggregated into the bundle-wide `missing_fields` report
4. Logged in the manifest for manual review

### Multi-Person Bundling
- **Primary person**: Full document set (common docs + role-specific contract)
- **Additional people**: Partial set (role-specific contract + declaration)
- Per-person contract type selection (General worker / Kitchen worker / Cleaner)
- Automatic filename deduplication for same-named individuals

---

## 5. REST API

### Process Management
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/process/start` | Start new extraction process |
| `GET` | `/api/v1/process/{id}/status` | Check process status/poll |
| `POST` | `/api/v1/process/{id}/verify` | Verify extracted data |
| `POST` | `/api/v1/process/{id}/cancel` | Cancel running process |
| `GET` | `/api/v1/process/{id}/download` | Download completed output |

### Document Management
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/documents/fill` | Generate document bundle |
| `GET` | `/api/v1/documents/{bundle_id}/download` | Download bundle ZIP |
| `GET` | `/api/v1/documents/{bundle_id}/manifest` | Download bundle manifest |
| `GET` | `/api/v1/documents/{bundle_id}/files/{name}` | Download single document |

---

## 6. Frontend

### User Interface
- **Glassmorphism design** with dark theme and backdrop blur effects
- **Three-module card layout**: Personal Data, Company Info, Documents Fulfillment
- **Responsive**: Adapts from desktop to mobile layouts
- **Animated transitions**: Fade-in effects, hover states, micro-interactions

### Session State
- **In-memory workflow state** per browser session
- Multi-person extraction with per-person file upload and name overrides
- Live editing of extracted data with missing-field highlighting
- Real-time status polling and cancellation for background processes
- Document contract type selection per person
