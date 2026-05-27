# AutoMate — Demo Video Script & Storyboard

> **Duration:** 2 minutes (120 seconds)
> **Style:** Clean screen recording with voiceover, subtle motion graphics, cinematic pacing
> **Audio:** Modern tech soundtrack (ambient/cinematic), low volume during narration
> **Resolution:** 1920×1080 @ 60fps, capture at 1.5x speed then slow to 1x for smooth cursor movement
> **Tone:** Professional, confident, polished — showcase engineering quality

---

## Scene 1 — Opening Hook (0:00–0:12)

| Time | Visual | Narration | Production Notes |
|------|--------|-----------|------------------|
| 0:00 | **Fade in from black** — Animated logo reveal: the AutoMate wordmark scales up with a subtle glow effect. Beneath it, a tagline fades in: *"Multi-Agent Document Intelligence Pipeline"* | **Narrator:** "Every business has paperwork. AutoMate turns messy documents into verified, legally-drafted outputs — automatically." | Use a clean motion graphics intro. No UI yet. Music rises from silence. |
| 0:07 | **Cut to full screen** — The AutoMate frontend dashboard, fully loaded. Dark glassmorphism theme. The three module cards (Personal Data, Company Info, Documents Fulfillment) are visible in their grid layout. Cursor moves gracefully across the screen. | **Narrator:** "This is AutoMate — an AI-powered platform that extracts, enriches, verifies, and generates legal documents in seconds." | Pre-load the page. Show state with a pristine empty session. |

---

## Scene 2 — Multi-Person Extraction (0:12–0:32)

| Time | Visual | Narration | Production Notes |
|------|--------|-----------|------------------|
| 0:12 | **Cursor clicks** the **Personal Data** module. A modal slides up (fade + translate). The upload UI is shown with 2 rows — each with a file picker, first name, and last name field — already populated (pre-fill for demo polish). | **Narrator:** "Start by uploading identity documents — passports, IDs, or even PDFs. AutoMate handles multiple people in a single session." | Use pre-populated upload rows for speed. Show 2 people: "Ana Petrova" and "Ivan Dimitrov". |
| 0:18 | **Cursor clicks "Start Extraction"**. A loading state appears — spinner overlay, pulsing progress bar. A status badge reads *"Processing..."* with a subtle animation. | **Narrator:** "Each document is processed in the background by our vision AI — GPT-4o-mini extracts names, dates, and identifiers with structured precision." | Record this at high FPS, then speed up 2x for pacing. |
| 0:24 | **Loading completes.** The modal shows results: extracted data fields for **Ana Petrova** — first name, last name, date of birth, nationality, document number — all populated. One field (middle name) shows the empty-state highlight with a soft red border. | **Narrator:** "Extracted data appears instantly — with missing fields clearly highlighted for review." | Pre-capture a successful extraction result. Keep the "missing field" highlight visible to demonstrate the validation UX. |
| 0:28 | **Cursor clicks "Confirm & Continue"**. The modal closes. A **"Pending Review"** badge briefly appears on the card (500ms), then transitions to a green checkmark badge with a subtle scale bounce. | **Narrator:** "This triggers LangGraph's interrupt-and-resume pattern — a human-in-the-loop verification gate that pauses the pipeline until the data is approved." | Show "Pending Review" → "Verified" badge transition to visually demonstrate the interrupt/resume pattern. |

---

## Scene 3 — Company Registry Lookup (0:32–0:52)

| Time | Visual | Narration | Production Notes |
|------|--------|-----------|------------------|
| 0:32 | **Cursor moves** to the **Company Info** card. Click. An input field expands with the label *"Company Registry Number (EIK)"*. The cursor types: `175306008` with a satisfying key-press effect (subtle scale animation on each character). | **Narrator (bridging):** "With people verified, we move to company enrichment. Enter the Bulgarian registry number — AutoMate's multi-strategy scraper handles the rest." | Use a real-looking EIK number. Show auto-typing effect. |
| 0:40 | **Cursor clicks "Look Up"**. A loading spinner appears. After 0.5s, a small badge reads *"Trying API..."*, then *"Fast path — Deeds API"* appears with a checkmark. The card populates with company name, legal form, registered address, manager name, contact info. | **Narrator:** "The system uses a smart fallback chain — Deeds API first for speed, then HTTP, then Playwright browser. Each strategy returns the same structured format." | Show fallback indicators in sequence. The "Fast path" badge emphasizes architecture without slowing the demo. |
| 0:48 | **Cursor hovers over** individual fields — tooltips appear showing source confidence and raw extracted value. The card expands to show a "View Raw Data" expandable section with a smooth height animation. | **Narrator:** "Every field is traceable — exactly where each value came from and how confident the system is." | A nice detail that shows engineering polish. Keep the tooltip visible for 2 seconds. |

---

## Scene 4 — Document Generation (0:52–1:16)

| Time | Visual | Narration | Production Notes |
|------|--------|-----------|------------------|
| 0:52 | **Cursor clicks** the **Documents Fulfillment** card. It expands with a smooth height transition. A list of 2 people appears, each with a dropdown labeled *"Contract Type"*. **Ana** has "General Worker" selected, **Ivan** has "Kitchen Worker" selected. | **Narrator:** "Now the real power — per-person document generation. Each person can have a different contract type: general worker, kitchen worker, cleaner." | Pre-select the contract types. Make the dropdown selection animation snappy. |
| 1:00 | **Cursor clicks "Generate Full Set"**. A loading overlay appears with a progress indicator: *"Generating documents... (3/8)"*. A brief badge flashes *"Processing: Договор - общ работник.docx"*. The counter ticks up rapidly. | **Narrator:** "AutoMate generates a complete bundle — common documents for the primary person, role-specific contracts for additional staff — each with proper naming and consistent formatting." | Capture at slow speed, then speed up 3x for the demo. The template-name badge adds engineering depth. |
| 1:08 | **Loading completes.** A success state appears: a download button with a file size badge (*"4.2 MB"*). Below it, a manifest list shows all generated documents with checkmarks: *"Service Agreement.docx"*, *"Employment Contract_Ana Petrova.docx"*, *"Condition Declaration_Ivan Dimitrov.docx"*. | **Narrator:** "A professionally-named, ready-to-distribute bundle — each document populated with verified data from the pipeline." | Scroll the file list with a smooth animation. Highlight the smart naming convention. |
| 1:12 | **Cursor clicks the download button.** A browser download notification appears at the bottom of the screen. The ZIP file name is visible: `AutoMate_Bundle_2026-05-27.zip`. | **Narrator:** "Download as a single ZIP — or access individual files through the API." | Capture the native browser download UI for authenticity. |

---

## Scene 5 — Architecture Reveal (1:16–1:36)

| Time | Visual | Narration | Production Notes |
|------|--------|-----------|------------------|
| 1:16 | **Screen transitions** to a clean dark slide. An animated pipeline diagram fades in: `INPUT → EXTRACTOR → VERIFICATION → SCRAPER → QA → SCRIBE → OUTPUT`. Each node lights up one by one with a glowing pulse animation, connected by flowing arrows. Current node highlighted in accent color. | **Narrator:** "Behind the scenes, AutoMate runs on a LangGraph-powered multi-agent pipeline." | Use a pre-rendered motion graphics animation. Each node lights up in sequence. |
| 1:24 | **Diagram zooms in** on the **EXTRACTOR** node. A small callout appears showing: *"GPT-4o-mini Vision"* and an icon of a passport with an eye/detection overlay. Pulse animation. | **Narrator:** "The vision extractor uses GPT-4o-mini to parse identity documents with structured output." | Smooth camera-style zoom transition (pan + scale). |
| 1:28 | **Diagram zooms out**, then a highlight ring appears around **SCRIBE**. A brief overlay shows a DOCX XML code snippet floating next to the node: `<w:r><w:t>Ana Petrova</w:t></w:r>` | **Narrator:** "The document engine works directly with OOXML — manipulating the XML inside DOCX files for precise control over formatting and layout." | Code snippet recognizable but too short to read fully. Represents engineering depth with confident, non-defensive framing. |
| 1:32 | **Final diagram state** — all nodes lit, a checkmark at OUTPUT. A subtle "Vercel-ready" badge appears at the bottom-right with the Vercel logo. | **Narrator:** "The entire system is cloud-native and Vercel-ready, with serverless-compatible fallbacks built in from day one." | Brand badge for recognition. |

---

## Scene 6 — Closing (1:36–2:00)

| Time | Visual | Narration | Production Notes |
|------|--------|-----------|------------------|
| 1:36 | **Screen splits** into a grid of 4 mini-animations playing simultaneously: | **Narrator:** "Key features at a glance — multi-person extraction, human-in-the-loop verification, smart error recovery, and a scalable architecture." | Dynamic grid layout. Subtle border highlight cycles through each quadrant in sequence. |
| | Top-left: Upload modal with 2 files | | |
| | Top-right: Verification gate confirmation dialog | | |
| | Bottom-left: Error state with retry button animation | | |
| | Bottom-right: Architecture diagram (mini) | | |
| 1:44 | **Grid collapses** to center — the screen shows a single card with key tech badges flying in with a staggered animation (80ms delay each): `Python` `FastAPI` `LangGraph` `OpenAI` `Pydantic v2` `Playwright` | **Narrator:** "Built with FastAPI, LangGraph, Pydantic v2, and Playwright — designed for real-world reliability." | Badge-style icons with staggered fly-in animation. |
| 1:50 | **Badges fade** into a single CTA card: *"Explore the architecture at github.com/yourusername/automate"* with a subtle pulsing arrow icon. Below it, three smaller links: *"Documentation"*, *"Sample Code"*, *"Technical Decisions"*. | **Narrator:** "The production implementation remains private, but the architecture, code samples, and technical decisions are fully open. Check it out on GitHub." | Clean, actionable end screen. CTA readable from thumbnail preview. |
| 1:56 | **Fade to black.** AutoMate logo + tagline fade in center. | **Narrator:** "AutoMate — intelligent document automation." | Hold for 5 seconds. Music fades out gently. |

---

## Appendix A: Production Checklist

### Pre-Recording Setup

- [ ] **Clean the frontend state** — start with a fresh browser session (no cached data)
- [ ] **Pre-load demo data** — have 2 passport images and a company EIK number ready
- [ ] **Set resolution** — record at 1920×1080, 60fps
- [ ] **Mouse cursor** — use a visible cursor enhancer (e.g., Mousepose for macOS) with a highlight circle on click
- [ ] **Browser zoom** — set to 110% for slightly larger UI elements
- [ ] **Disable notifications** — turn off all OS and browser notifications
- [ ] **Pre-warm** — run the extraction once before recording so it's fast on the take
- [ ] **Audio** — use a quality condenser microphone; record at 48kHz/24bit
- [ ] **Room tone** — capture 10 seconds of silence for noise reduction in post

### Post-Production

- [ ] **Speed ramps** — speed up extraction loading 2–3x, keep cursor movements at 1x
- [ ] **Cursor glow** — add a subtle glow/highlight around the cursor in post
- [ ] **Transitions** — use smooth crossfades (0.3s) between scenes, avoid hard cuts
- [ ] **Lower thirds** — add subtle lower-third labels for tech terms (e.g., "LangGraph", "GPT-4o-mini")
- [ ] **Color grade** — slight cool tint to match the dark glassmorphism theme
- [ ] **Captions** — add clean white-on-dark captions for accessibility; YouTube-style
- [ ] **End card** — YouTube end card with subscribe/watch-more elements

### Audio Mix

| Element | Level | Notes |
|---------|-------|-------|
| Voiceover | -6 dB | Center panned, light compression (3:1 ratio), no reverb |
| Background music | -20 dB | Ambient/cinematic, duck to -28 dB during narration |
| Sound effects | -12 dB | Subtle UI clicks, whooshes for transitions only |
| Room tone | -60 dB (noise floor) | Use noise gate to remove silence hiss |

### Delivery Formats

- **Primary**: YouTube / Vimeo — H.264, 1080p, 60fps, AAC 192kbps
- **Thumbnail**: 1280×720, dark background, AutoMate logo in center, tagline below
- **Short clip**: 30-second cutdown for LinkedIn/Twitter — focus on scenes 2 and 4
- **GIF preview**: 15-second loop of document generation (scene 4) for README

---

## Appendix B: Suggested Thumbnail Design

```
┌─────────────────────────────────────────────────────────┐
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░                                               ░░   │
│  ░░        [AutoMate Logo - Large, Centered]       ░░   │
│  ░░          Multi-Agent Document Pipeline         ░░   │
│  ░░                                               ░░   │
│  ░░     ┌──────────────────────────────────┐      ░░   │
│  ░░     │  Passport Image → [AI] → DOCX   │      ░░   │
│  ░░     │  (Animated processing glow)     │      ░░   │
│  ░░     └──────────────────────────────────┘      ░░   │
│  ░░                                               ░░   │
│  ░░     [▶] 2:00 • Python • FastAPI • LangGraph  ░░   │
│  ░░                                               ░░   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
└─────────────────────────────────────────────────────────┘
```

---

## Appendix C: Script Variations

### 30-Second Social Cut

| Time | Scene | Narration |
|------|-------|-----------|
| 0:00 | Dashboard → Upload passports | "Upload identity documents — AutoMate extracts structured data with AI." |
| 0:08 | Company lookup | "Enter a registry number — our multi-strategy scraper fetches company data." |
| 0:16 | Document generation | "Generate complete, legally-drafted document bundles with one click." |
| 0:24 | Architecture + CTA | "LangGraph-powered, Vercel-ready. Full architecture on GitHub." |

### Silent / Walkthrough Version (No Narration)

- Add clean on-screen text annotations (motion typography) instead of voiceover
- Use subtle sound effects for each interaction
- Include a progress bar at the bottom showing "Personal Extraction → Company Lookup → Document Generation"
- End with a QR code linking to the GitHub repo
