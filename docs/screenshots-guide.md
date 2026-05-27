# Screenshots & Visual Portfolio Guide

> A guide to capturing visual materials for the AutoMate portfolio showcase.

---

## Recommended Screenshots

### 1. Home Dashboard
**File:** `screenshots/home-dashboard.png`
**What to capture:**
- The glassmorphism home page with three action cards
- The dark theme with gradient accents
- Hover state on one of the cards (showing the purple glow)

### 2. Personal Extraction Modal
**File:** `screenshots/personal-extraction.png`
**What to capture:**
- Modal showing the multi-person upload interface
- Status card on the left
- Extracted data preview on the right
- The file picker and name override fields

### 3. Extracted Data Editor
**File:** `screenshots/data-editor.png`
**What to capture:**
- Expanded person card showing all extracted fields
- Missing field highlighting (red borders)
- Multiple collapsed/expanded person cards
- The missing-badge count indicators

### 4. Company Registry Results
**File:** `screenshots/company-data.png`
**What to capture:**
- Company info modal with filled data
- The structured company data in editable fields
- Status showing "Completed"

### 5. Document Generation Results
**File:** `screenshots/document-generation.png`
**What to capture:**
- Documents modal with generated bundle results
- The contract selection cards per person
- Download links for individual documents
- Missing fields report

### 6. Pipeline Flow Animation
**File:** `screenshots/pipeline-flow.gif`
**What to capture:**
- Animated GIF showing the extraction → verification → generation flow
- For best results, record a complete flow from start to finish
- Use a screen recording tool that produces clean GIFs

---

## GIF Recording Recommendations

| Tool | Platform | Quality |
|---|---|---|
| **CleanShot X** | macOS | Excellent |
| **ScreenToGif** | Windows | Great |
| **Kap** | macOS | Good (free) |
| **Peek** | Linux | Good (free) |

**Settings:**
- Frame rate: 10-15 fps
- Width: 800-1200px
- Color palette: optimize for web
- Duration: 8-15 seconds

---

## Architecture Diagrams

### Mermaid Diagrams (In Code)

The `docs/architecture.md` file contains Mermaid diagrams that render automatically on GitHub. These include:

1. **Pipeline Flow Diagram** — Shows the agent graph with conditional routing
2. **Deployment Architecture** — Shows Vercel, database, and external services

### Custom Diagrams (Optional)

You may want to create high-resolution versions of:

| Diagram | File | Description |
|---|---|---|
| System Architecture | `diagrams/system-architecture.png` | Full layer diagram |
| Agent Pipeline | `diagrams/agent-pipeline.png` | LangGraph node flow |
| Data Flow | `diagrams/data-flow.png` | How data moves through the system |

**Recommended tools for custom diagrams:**
- **draw.io** (free, web-based)
- **Excalidraw** (hand-drawn style)
- **Figma** (professional, collaborative)

---

## Repository Social Preview

GitHub uses a social preview image (1280×640px) for link sharing:

**File:** `public-assets/social-preview.png`

**Suggested design:**
- Dark background (matches the app theme)
- "AutoMate" in gradient text (purple to blue)
- Tagline: "Multi-Agent Document Intelligence Pipeline"
- Subtle graph/flow icon on the right
- Tech stack logos along the bottom

---

## Screenshot Requirements Summary

| Asset | Format | Resolution | Priority |
|---|---|---|---|
| Home Dashboard | PNG | 1200×800 | High |
| Personal Extraction | PNG | 1400×900 | High |
| Data Editor | PNG | 1400×900 | High |
| Company Data | PNG | 1200×800 | Medium |
| Document Generation | PNG | 1600×900 | High |
| Pipeline Flow | GIF | 1000×700 | Medium |
| Social Preview | PNG | 1280×640 | Low |
| Architecture Diagram | PNG | 1600×900 | Medium |
