# 📞 VoxLog — Voicemail Transcription Dashboard

> A single-file HTML5 SPA for transcribing, organizing, and managing voicemail recordings. No installation, no server, no dependencies to install — just open the file in a browser.

![VoxLog Dashboard](https://img.shields.io/badge/version-1.0-00c896?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square) ![Built with](https://img.shields.io/badge/built%20with-HTML%2FJS%2FCSS-orange?style=flat-square)

---

## Overview

VoxLog lets you drop a folder of `.wav` voicemail recordings into a browser, transcribe them automatically using AI, and manage the results in an editable dashboard. Everything runs locally in your browser — the only external calls are to the Groq API for transcription and metadata extraction.

**Key capabilities:**
- Batch transcription of `.wav` files via Groq Whisper
- Automatic extraction of caller name, phone number, and call date from transcript text
- Fully editable dashboard with inline cell editing
- Status tracking per voicemail (Pending / In Progress / Done)
- Save/load session state as a real SQLite `.db` file
- Export to CSV for use in Excel or Google Sheets
- Full-text search and multi-column sort
- Zero install — single `.html` file, runs in any modern browser

---

## Requirements

- A modern browser (Chrome, Edge, Firefox)
- A free **Groq API key** — get one at [console.groq.com](https://console.groq.com)
- Your voicemail recordings in `.wav` format

---

## Quick Start

1. Open `[https://lanceterrill.github.io/VoxLog/]` in your browser
2. Enter your Groq API key in the modal (or click **Skip** for demo mode)
3. Click **📁 Load WAV Files** or drag-and-drop `.wav` files onto the drop zone
4. Click **⚡ Transcribe All** — each file is sent to Groq Whisper
5. Review auto-filled caller info, edit anything as needed
6. Click **💾 Save .db** to save your session for next time

---

## How It Works

### Transcription Pipeline

Each `.wav` file goes through a two-step AI pipeline:

**Step 1 — Groq Whisper (`whisper-large-v3-turbo`)**
The audio file is read as binary, manually encoded into a `multipart/form-data` byte array (avoiding `FormData` which is blocked in sandboxed iframes), and posted to `https://api.groq.com/openai/v1/audio/transcriptions`. Returns verbatim transcript text.

**Step 2 — Groq LLaMA (`llama3-8b-8192`)**
The transcript is passed to a chat completion with a structured prompt that extracts:
- **Caller identity** — name, org, department, or role
- **Phone number** — the callback number left in the message
- **Call date/time** — any date or time mentioned in the transcript

Both steps run sequentially per file during batch transcription.

### Caller Name Extraction

This was the most iterated piece of the app. The logic uses two layers:

**LLM layer (primary):** A carefully engineered prompt instructs the model to identify the *speaker* — not the person being called. It follows a priority chain:

1. Name + org → `"Stuart @ Broadcast House"`
2. Name only → `"Stuart"`
3. Org/company only → `"[Broadcast House]"`
4. Department only → `"[Billing Dept]"`
5. Role/title only → `"[Your Insurance Agent]"`
6. Nothing identifiable → `""`

The prompt explicitly distinguishes self-identification phrases (`"this is X"`, `"X here"`, `"X calling"`, `"X over here at Y"`) from recipient phrases (`"calling for X"`, `"Hey X"`, `"trying to reach X"`) which are never the caller.

**Regex fallback (secondary):** Used when no API key is present or the LLM returns empty. Strips recipient phrases from the transcript first, then applies strict pattern matching against self-ID patterns only. No guessing — blank is always preferred over wrong.

### Date Parsing

Call date/time is populated from two sources:
- **Filename parsing** — many voicemail systems name files by timestamp (e.g. `20240314_143022.wav`, `031126.wav`). VoxLog parses these automatically when files are loaded.
- **Transcript extraction** — the LLM extracts any spoken date or time reference from the message text.

### Save / Load (.db)

VoxLog uses [sql.js](https://github.com/sql-js/sql.js/) (SQLite compiled to WebAssembly) to read and write real `.db` files entirely in the browser — no server required.

**Saving:** All voicemail records are written into a SQLite table and exported as a binary `.db` file download.

**Loading:** A `.db` file is read back into memory, parsed by sql.js, and the dashboard is restored exactly as it was left — all transcriptions, edits, caller info, notes, and statuses intact.

> **Note:** The original `.wav` audio files are not stored in the `.db` — only the text data. To re-transcribe a file you'll need the original audio.

The `.db` file is a standard SQLite database and can be opened in any SQLite tool such as [DB Browser for SQLite](https://sqlitebrowser.org/).

---

## Dashboard Reference

### Toolbar

| Button | Function |
|--------|----------|
| 📁 Load WAV Files | Open file picker for `.wav` files (also supports drag-and-drop) |
| ⚡ Transcribe All | Batch transcribe all un-transcribed files |
| ⬇ Export CSV | Download all rows as `voxlog_export.csv` |
| 💾 Save .db | Save full session to `voxlog.db` (SQLite) |
| 📂 Load .db | Restore a previously saved session |
| ✕ Clear All | Wipe the dashboard (with confirmation) |

### Editable Columns

| Column | Auto-filled | Description |
|--------|-------------|-------------|
| Phone Number | ✓ from transcript | Callback number the caller leaves. Primary sort key. |
| Caller Name | ✓ from transcript | Speaker identity — name, org, dept, or role. See extraction logic above. |
| Call Date/Time | ✓ from filename or transcript | Timestamp parsed from filename or spoken in message. |
| Filename | — | Original `.wav` filename (display only) |
| Transcription | ✓ via Whisper | Full verbatim transcript. Fully editable. |
| Notes | — | Free-form notes — follow-up actions, flags, context. |
| Status | — | Dropdown: Pending / In Progress / Done |

All cells are inline-editable — click any field to type. Changes are reflected in the next `.db` save or CSV export.

### Status Values

| Status | Meaning |
|--------|---------|
| 🔵 Pending | Default. Not yet reviewed. |
| 🟡 In Progress | Being worked on or awaiting follow-up. |
| 🟢 Done | Resolved. No further action needed. |

### Sort & Search

- **Search bar** — filters across all columns: phone, caller, transcript text, notes, date, filename
- **Sort dropdown** — sort by phone number (default), call date (oldest/newest), caller name, filename, or status

---

## Development History

### v1.0 — Initial Build

- Single-file HTML SPA created from scratch
- Anthropic Claude API used initially for transcription via `document` block — **failed** with error: `Input should be 'application/pdf'` (Claude API does not accept audio via document blocks)

### Transcription Engine: Claude → OpenAI Whisper → Groq Whisper

**Attempt 1 — Claude API (Anthropic)**
Used `document` type with base64-encoded WAV. Rejected — Claude's document block only accepts PDF.

**Attempt 2 — OpenAI Whisper**
Switched to `https://api.openai.com/v1/audio/transcriptions`. Hit a second issue: `FormData` objects cannot be cloned across iframe boundaries in sandboxed environments, causing a `postMessage` error. Resolved by manually constructing the multipart body as a raw `Uint8Array` instead of using `FormData`.

OpenAI Whisper worked, but required a paid account. Users on the free tier received quota errors.

**Attempt 3 — Groq Whisper (current)**
Switched endpoint to `https://api.groq.com/openai/v1/audio/transcriptions` using `whisper-large-v3-turbo`. Same manual multipart encoding retained. Groq's free tier is generous and the model is faster and more accurate than OpenAI's `whisper-1`.

### Status System Redesign

Original statuses: `new / reviewed / actioned / archived` (click-to-cycle badge)

Replaced with: `pending / in-progress / done` (dropdown selector inside styled badge) — cleaner workflow terminology, more intuitive for a voicemail triage use case.

### Caller Name Extraction — Iteration History

This feature went through the most revision of anything in the app:

**Round 1** — Regex only. Patterns like `/(?:this is|my name is)\s+([A-Z][a-z]+)/`. Too loose — matched recipient names after "calling for".

**Round 2** — Added LLM extraction via Groq LLaMA. Prompt was too vague about the caller/recipient distinction. Still picked up wrong names (e.g. `"Hey Jonathan"` → `Jonathan`).

**Round 3** — Explicit examples added to prompt. Still failed on names after "calling for".

**Round 4** — Prompt rewritten to explicitly enumerate recipient trigger words (`"for"`, `"to reach"`, `"Hey X"`). Regex fallback updated to strip recipient phrases before pattern matching.

**Round 5** — Tightened to `blank unless certain`. Removed last-resort greedy patterns from regex. LLM instructed to default to `""` on any ambiguity.

**Round 6 (current)** — Full context-clue system added. Caller field now populated using a priority chain: name+org → name → [org] → [dept] → [role] → blank. Handles patterns like `"Stuart over here at Broadcast House"` → `Stuart @ Broadcast House`, and `"calling from the billing department"` → `[Billing Dept]`.

### Save/Load System

Added sql.js (SQLite via WebAssembly) for persistent session storage. Chose `.db` over localStorage (size limits) and JSON (not reopenable in external tools). The `.db` file is a standard SQLite database compatible with DB Browser for SQLite, Python's `sqlite3`, and any other SQLite client.

---

## File Structure

```
voicemail-dashboard.html    # The entire application — HTML, CSS, JS in one file
voxlog.db                   # Your saved session (generated by the app)
voxlog_export.csv           # CSV export (generated by the app)
```

---

## External Dependencies (CDN)

| Library | Version | Purpose |
|---------|---------|---------|
| [sql.js](https://github.com/sql-js/sql.js/) | 1.10.2 | SQLite in WebAssembly for .db save/load |
| [IBM Plex Mono / Sans](https://fonts.google.com/specimen/IBM+Plex+Mono) | — | UI typography |
| [Groq API](https://console.groq.com) | — | Whisper transcription + LLaMA metadata extraction |

No npm, no build step, no framework. Everything else is vanilla HTML/CSS/JS.

---

## API Usage & Cost

| Service | Model | Cost |
|---------|-------|------|
| Groq Whisper | `whisper-large-v3-turbo` | Free tier — generous limits |
| Groq LLaMA | `llama3-8b-8192` | Free tier — metadata extraction per voicemail |

Both calls use your Groq API key (`gsk_...`). Get one free at [console.groq.com](https://console.groq.com).

---

## Privacy

- Audio files are sent to Groq's API for transcription. Review [Groq's privacy policy](https://groq.com/privacy-policy/) if handling sensitive voicemails.
- Your API key is stored in memory only — never written to disk, localStorage, or sent anywhere other than Groq's API.
- All other data (transcripts, notes, statuses) stays entirely in your browser and in the `.db` file you control.

---

## License

MIT — use it, modify it, deploy it however you like.
