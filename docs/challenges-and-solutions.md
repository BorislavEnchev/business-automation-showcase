# Challenges & Solutions

> Real engineering challenges encountered during development and how they were solved.

---

## Challenge 1: Registry Scraping in Serverless Environments

### The Problem
The Bulgarian Commercial Registry is a JavaScript-heavy SPA. Playwright (the browser automation tool) cannot run in Vercel's serverless functions. The initial approach — render the page with Playwright, extract text — only worked locally.

### The Solution
**Multi-strategy fallback chain** with automatic environment detection:

1. **Deeds API** (internal JSON endpoint) — SPA loads data from this endpoint, so we call it directly
2. **HTTP GET + html-to-text** — fetch the raw HTML, strip tags, extract text
3. **CompanyBook API** — third-party company data API for basic metadata
4. **Playwright browser** — final fallback for local development only

Each strategy returns a normalized `{raw_text, source, company_hint}` dict. The graph routes accordingly.

### Key Insight
Most SPAs load data from internal APIs that are accessible without JavaScript. Inspecting network traffic revealed the Deeds API endpoint — it returns data as JSON embedded in the page, which we could parse without any browser rendering.

---

## Challenge 2: Bilingual Document Template Filling

### The Problem
The legal templates are bilingual (Bulgarian/English) with complex formatting:
- Mixed bold/normal text in the same paragraph
- Right-aligned signature blocks with specific tab stops
- Tables with EN on left, BG on right
- Date formats differ between languages
- Some fields need transliteration, others need actual translation

Existing DOCX libraries couldn't handle the complexity.

### The Solution
**Custom OOXML transformation engine** that works directly with the XML inside `.docx` files:

```python
# Pattern: open as ZIP → parse XML → transform → re-zip
with zipfile.ZipFile(source_path, "r") as source_zip:
    xml_bytes = source_zip.read("word/document.xml")
    root = ET.fromstring(xml_bytes)

    # Apply per-template transforms
    for paragraph in root.findall(".//w:p", NS):
        text = get_paragraph_text(paragraph)
        updated = transform(text, context)
        if updated != text:
            set_paragraph_text(paragraph, updated)

    # Re-zip with modified XML
    with zipfile.ZipFile(output_path, "w", ...,) as output_zip:
        output_zip.writestr("word/document.xml", updated_xml)
```

For complex layouts, we bypass text-level transforms and manipulate the XML structure directly — injecting runs, adjusting tab stops, and merging table rows.

### Key Insight
OOXML is surprisingly approachable when you work at the right abstraction level. The key was building helper functions (`_set_paragraph_text`, `_add_run`, `_set_paragraph_rich_text`) that encapsulate namespace-aware XML manipulation, and then composing document-specific transforms on top of them.

---

## Challenge 3: Multi-Person Document Bundling

### The Problem
Legal workflows often involve multiple employees being hired at once. Each person needs:
- A full document set (for the primary person)
- A partial set (for additional people)
- Per-person contract type selection (General, Kitchen, Cleaner)
- Unique filenames that include person names
- A single downloadable bundle

### The Solution
**Flexible template mapping system:**

```python
PROFESSION_CONTRACT_MAP = {
    "general_worker": "Договор  - общ работник.docx",
    "kitchen_worker":  "Договор - работник кухня.docx",
    "cleaner":         "Договор - чистач хигиенист.docx",
}

# First person: common templates + selected contract
# Additional people: selected contract + declaration only
def _should_skip_template(template_name, contract_type, person_index):
    # Rules per person index
```

The `generate_multi_person_document_bundle` function iterates over people, applying different `template_names` sets based on person index, while sharing a single output directory and ZIP bundler.

### Key Insight
The template selection logic is a simple mapping problem — not complex when separated from the rendering engine. The real complexity was in ensuring unique filenames for same-named people and maintaining backwards compatibility with the single-person flow.

---

## Challenge 4: Date Normalization From Unstructured Input

### The Problem
Passport scans and registry data produce dates in various formats:
- `20.05.1985` (Bulgarian format)
- `05/20/1985` (US format)
- `1985-05-20` (ISO format)
- `Unknown`, `N/A`, `none`, `not visible` (missing values)
- OCR errors producing month=00 or day=99

Invalid dates would cause Pydantic validation to fail the entire extraction.

### The Solution
**Multi-stage normalization pipeline:**

```python
def _normalize_date_value(value, fallback="1900-01-01"):
    # 1. Check for missing value markers
    if not value or value.lower() in MISSING_MARKERS:
        return fallback

    # 2. Try multiple date formats
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return text  # Already in YYYY-MM-DD
```

Followed by Pydantic validation that accepts the normalized format. Unknown dates become `1900-01-01` — a sentinel value that the frontend can detect and flag.

### Key Insight
Don't fail on bad input — normalize aggressively, validate the structure, and let the UI highlight what needs attention. The sentinel pattern (`1900-01-01` for missing dates) is more actionable than a validation error buried in logs.

---

## Challenge 5: Extracting Clean Data From Corrupted Text

### The Problem
The Bulgarian Commercial Registry's data frequently suffers from:
- **Mojibake** (encoding corruption): `Ð½Ð°ÑÐµÐ»ÐµÐ½Ð¾` instead of `населено`
- **JSON leakage**: raw JSON fragments mixed into company names
- **HTML garbage**: escaped HTML entities in text fields
- **Concatenated identifiers**: company numbers and phone numbers merged together

### The Solution
**Repair pipeline before parsing:**

```python
def _repair_mojibake(text):
    if "Ð" in text or "Ñ" in text:
        # Attempt latin1 → utf-8 re-encoding
        repaired = text.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
        # Only use if it produces more Cyrillic characters
        if cyrillic_count(repaired) > cyrillic_count(text):
            return repaired
    return text
```

Plus LLM cleanup as a final safety net — if the deterministic parser detects JSON fragments in extracted names, it delegates to GPT-4o-mini for structural cleanup.

### Key Insight
When dealing with real-world data sources, assume corruption. Build a repair pipeline that gradually escalates fidelity — try the cheapest fix first, use the LLM as a last resort. This keeps costs low while catching edge cases.

---

## Challenge 6: Human-in-the-Loop Without Complexity

### The Problem
Human verification is essential for legal document accuracy, but implementing it typically requires:
- A state machine with "waiting for approval" states
- Persistent storage for pending approvals
- An approval API with timeout handling
- Retry logic for expired approvals

### The Solution
**LangGraph's `interrupt()` pattern** handles all of this out of the box:

```python
async def verification_gate_node(state):
    # Pause execution — return control to the API layer
    human_input = interrupt({
        "person_data": person,
        "action_required": "POST /process/{id}/verify with is_verified=true"
    })

    # Execution resumes here when the human responds
    is_verified = human_input.get("is_verified", False)
    # ... proceed or fail based on response
```

The API layer wraps this with:
- An endpoint that resumes the graph with the verification decision
- State persistence after each interruption
- Process cancellation that kills the running task

### Key Insight
The graph-based approach inverts the problem. Instead of building a system that checks "is there pending approval?", the system simply *stops executing until told to continue*. This eliminates polling, timeout logic, and state synchronization.
