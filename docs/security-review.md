# Security & Privacy Review

> Review of what the showcase repository exposes, what remains private,
> and recommendations for maintaining separation.

---

## What This Showcase Exposes

### Safe Public Content ✅

| Category | Content |
|---|---|
| **Architecture** | Layer diagrams, Mermaid flowcharts, data flow descriptions |
| **Design Patterns** | Graph orchestration, strategy pattern, HITL pattern |
| **Schema Contracts** | Pydantic field definitions (without business rules) |
| **API Routes** | Endpoint signatures with sanitized examples |
| **Code Patterns** | Agent node structure, graph routing, transform pipeline |
| **Tech Stack** | Languages, frameworks, libraries used |
| **Challenges** | General problem descriptions with sanitized solutions |
| **Frontend** | Complete UI code (HTML/CSS/JS) — application-level only |

### Sanitized Content ⚠️

| Category | How It's Sanitized |
|---|---|
| **Extractor Logic** | Document extraction prompt shown, but actual system prompt removed |
| **Scraping Logic** | Strategy pattern shown, actual registry URLs/parsers removed |
| **Document Templates** | Transform patterns shown, no actual legal template text |
| **Company Data** | Schema shown, no real company data or Balkan Fortune defaults |
| **Database** | ORM patterns shown, actual connection strings removed |

## What Remains Private 🔒

### MUST REMAIN PRIVATE

| Category | Reason | Location in Production |
|---|---|---|
| **OpenAI API Key** | Credential exposure | `.env.local`, environment variables |
| **Database URLs** | Infrastructure credential | `.env.local`, environment variables |
| **Secret Keys** | Security credential | `app/core/config.py` |
| **DOCX Templates** | Proprietary legal content | `app/services/documents/templates/` |
| **Real Company Data** | Business-sensitive | `app/services/documents/engine.py` (BALKAN_FORTUNE) |
| **Full Scraping Code** | Complete registry-specific logic | `app/agents/scraper.py` |
| **Actual System Prompts** | Proprietary extraction instructions | `app/agents/extractor.py` |
| **User Data** | Production data privacy | Database |

---

## File Classification

### Production Files NOT Included in Showcase

These files from the production repository are **entirely omitted**:

```
# Templates — proprietary legal content
app/services/documents/templates/

# Environment — credentials and secrets
.env.local
.env

# Full source — proprietary business logic
app/agents/scraper.py
app/services/scraping/playwright_service.py
app/services/documents/engine.py

# Database — no actual data included
*.db
```

### Production Files Adapted for Showcase

These files were **adapted (sanitized)** for public display:

| Production File | Showcase Equivalent | Changes Made |
|---|---|---|
| `app/schemas/person.py` | `sample-code/person_schema.py` | Removed business-specific validators, added generalized examples |
| `app/services/automation/graph.py` | `sample-code/graph_routing.py` | Abstracted routing logic, removed internal references |
| `app/agents/extractor.py` | `sample-code/extractor_agent.py` | Simplified, removed system prompt and OpenAI call |
| `app/services/documents/engine.py` | `sample-code/docx_transform.py` | Generalized, removed document-specific transforms |
| `app/api/v1/endpoints/process.py` | `sample-code/api_routes.py` | Simplified, removed background task management |

---

## Recommendations

### 1. Maintain Separate Repositories
- Keep the **production repository** private (GitHub private repo)
- This **showcase repository** should be a separate public repo
- Never push production commits to the showcase repo

### 2. Add a GitHub Secret Scanning Policy
- Configure GitHub to scan for API keys and tokens
- Set up branch protection on the showcase repo

### 3. Consider a Lightweight Demo Version
- For maximum impact, create a **deployed demo** on Vercel
- The demo could use mock data with a sample workflow
- No API keys needed — the frontend + mock API can demonstrate the UX

### 4. Standalone OSS Component Opportunities
The following components could be extracted as independent open-source libraries:

| Component | Potential Library |
|---|---|
| **OOXML Paragraph Helpers** | Lightweight Python library for DOCX paragraph manipulation |
| **Date Normalizer** | Agnostic date parser for European/Bulgarian formats |
| **Multi-Strategy Scraper Base Class** | Abstract scraper with fallback chain pattern |

### 5. Future Updates
When updating the showcase:
- Review new code additions for sensitive content
- Re-sanitize sample code if patterns change significantly
- Update screenshots if the UI evolves
- Keep the README aligned with the current architecture
