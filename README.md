# 📞 VoxLog
### *Voicemail Transcription & List Sync Dashboard*

> **Drop it. Transcribe it. Push it.** — A zero-install, single-file HTML tool that turns raw `.wav` voicemail recordings into structured, searchable, actionable records — synced directly to Microsoft Lists via Power Automate.

![Version](https://img.shields.io/badge/version-1.0-00c896?style=flat-square&logo=github)
![License](https://img.shields.io/badge/license-MIT-0099ff?style=flat-square)
![Built With](https://img.shields.io/badge/built%20with-HTML%20%2F%20JS%20%2F%20CSS-ffaa00?style=flat-square)
![Powered By](https://img.shields.io/badge/powered%20by-Groq%20Whisper-ff4455?style=flat-square)
![No Install](https://img.shields.io/badge/no%20install-just%20open-00c896?style=flat-square)

---

## ✨ What It Does

```
┌─────────────────────────────────────────────────────────────┐
│                        VOXLOG FLOW                          │
│                                                             │
│  🎙️ .wav files  →  ⚡ Whisper AI  →  📋 Dashboard         │
│                                                             │
│  📋 Dashboard   →  📤 Push to List  →  📧 Email            │
│                                                              │
│  📧 Email       →  🤖 Power Automate  →  📊 MS List        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Features at a Glance

| Feature | Description |
|---------|-------------|
| 🎙️ **Batch Transcription** | Drop a whole folder of `.wav` files, transcribe all at once |
| 🧠 **AI Metadata Extraction** | Caller name, phone number, and call date pulled automatically |
| ✏️ **Inline Editing** | Every field editable directly in the table — no forms, no popups |
| 📅 **Date & Time Pickers** | Call Date, Call Time, Returned Date, Returned Time |
| 🔄 **Status Tracking** | Pending → In Progress → Review → Done → Unreachable |
| 💾 **SQLite Backup** | Save and reload full sessions as `.db` files |
| 📊 **CSV Export** | Full export for Excel / Google Sheets analysis |
| 📤 **Push to MS List** | One-click sync to Microsoft List via Power Automate |
| ✅ **Pushed Flag** | Green ✓ tracks which records have been synced |
| 🔍 **Search & Sort** | Full-text search across all columns, multi-column sort |
| 🌙 **Dark / Light Mode** | Persistent theme toggle |
| 📵 **Zero Install** | Single `.html` file — just open it in a browser |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        AUTOMATED LANE                            │
│                                                                  │
│  📥 Outlook Shared    →   🤖 Power Automate    →   📊 VoxLog    │
│     Mailbox               Cloud Flow                MS List      │
│  DOI.SHIP@...             (Standard connectors)                  │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                         MANUAL LANE                              │
│                                                                  │
│  🎙️ WAV Files    →   ⚡ Groq Whisper   →   🧠 LLaMA Meta        │
│                                                                  │
│  📋 VoxLog           →   ✏️ Staff Review    →   📤 Push          │
│     Dashboard             & Edit                to List          │
└──────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Start

```
1. 🌐  Open  →  lanceterrill.github.io/VoxLog
2. 🔑  Enter your Groq API key  (console.groq.com → free)
3. 📁  Load WAV Files  →  drag & drop or file picker
4. ⚡  Transcribe All  →  AI fills caller, phone, date
5. ✏️  Review & edit  →  click any cell
6. 📤  Push to List  →  email JSON → Power Automate → Done
```

---

## 📋 Dashboard Columns

> Mirrors the **VoxLog Microsoft List** schema exactly — what you see is what gets pushed.

| Column | Auto-filled | Editable | Notes |
|--------|:-----------:|:--------:|-------|
| 📞 Phone Number | ✅ from transcript | ✅ | Primary sort key |
| 👤 Caller Name | ✅ from transcript | ✅ | AI priority chain |
| 📅 Call Date | ✅ at transcription | ✅ date picker | YYYY-MM-DD |
| 🕐 Call Time | ✅ at transcription | ✅ time picker | HH:MM |
| 📄 Filename | — | ✅ | Timestamped unique label |
| 📝 Transcription | ✅ via Whisper | ✅ | Full verbatim text |
| 👷 Staff Name | — | ✅ | Free text |
| 📅 Returned Date | — | ✅ date picker | When callback made |
| 🕐 Returned Time | — | ✅ time picker | When callback made |
| 🗒️ Notes | — | ✅ | Free-form |
| 🔵 Status | — | ✅ dropdown | 5 values |

---

## 🔄 Status Lifecycle

```
  🔵 Pending  →  🟡 In Progress  →  🩷 Review  →  🟢 Done
                                              ↘  🔴 Unreachable
```

---

## 🧠 AI Extraction Pipeline

```
┌─────────────────────────────────────────────────────────┐
│              CALLER NAME PRIORITY CHAIN                 │
│                                                         │
│  1️⃣  Name + Org   →  "Stuart @ Broadcast House"        │
│  2️⃣  Name only    →  "Stuart"                          │
│  3️⃣  Org only     →  "[Broadcast House]"               │
│  4️⃣  Department   →  "[Billing Dept]"                  │
│  5️⃣  Role/Title   →  "[Your Insurance Agent]"          │
│  6️⃣  Nothing      →  ""  (blank beats wrong)           │
│                                                         │
│  ❌  NEVER uses: "calling for X", "Hey X", "reach X"   │
└─────────────────────────────────────────────────────────┘
```

**Two-layer extraction:**
- 🤖 **Groq LLaMA** (`llama3-8b-8192`) — primary, structured JSON prompt
- 🔤 **Regex fallback** — fires when no API key or LLM returns empty

---

## 📤 Push to List — How It Works

```
┌─────────┐    ┌──────────┐    ┌────────────┐    ┌──────────────┐
│ VoxLog  │    │  JSON    │    │  Outlook   │    │    Power     │
│Dashboard│───▶│ Download │───▶│   Email    │───▶│  Automate   │
│         │    │(unpushed)│    │DOI.SHIP@...│    │  Flow       │
└─────────┘    └──────────┘    └────────────┘    └──────┬───────┘
                                                         │
                                                         ▼
                                                  ┌─────────────┐
                                                  │  VoxLog     │
                                                  │ Microsoft   │
                                                  │    List     │
                                                  └─────────────┘
```

**Power Automate Flow (Standard Connectors Only):**

```
Trigger  →  Compose         →  Parse JSON  →  Apply to each  →  Create item
Shared       base64ToString     flat array     11 fields          VoxLog List
Mailbox V2   attachment
```

> 📧 Subject must be exactly: **`VoxLog List Sync`**
> 🔒 Standard M365 connectors only — no premium, no HTTP action

---

## 💾 Save & Restore

| Format | Purpose | Reloadable | Opens in Excel |
|--------|---------|:----------:|:--------------:|
| 💾 `.db` | Save & restore full session | ✅ | ❌ |
| 📊 `.csv` | Share / analyze in spreadsheet | ❌ | ✅ |
| 📄 `.json` | Push to MS List via PA flow | ❌ | ❌ |

---

## 🛠️ Technical Stack

```
┌─────────────────────────────────────────────────────┐
│  🌐 Frontend    │  Vanilla HTML / CSS / JS           │
│  🗄️ Database    │  sql.js (SQLite via WebAssembly)   │
│  🎙️ Transcribe  │  Groq Whisper large-v3-turbo       │
│  🧠 Metadata    │  Groq LLaMA 3 8B                   │
│  🔄 Sync        │  Power Automate (standard only)    │
│  📦 Deploy      │  GitHub Pages (single HTML file)   │
│  🔑 Auth        │  Session only — never saved        │
└─────────────────────────────────────────────────────┘
```

**Zero dependencies to install.** Everything runs in the browser.
External CDN: `sql.js 1.10.2` · `IBM Plex Mono/Sans` (Google Fonts)

---

## 🔒 Privacy & Security

- 🎙️ Audio sent to **Groq API only** for transcription
- 🔑 API key stored **in memory only** — never written to disk or localStorage
- 📋 All transcription data stays in **your browser** and `.db` file
- 🏛️ Built for **NDOI / OCIO M365 GovCloud** (`stateofne.sharepoint.com`)

---

## 📁 Repo Structure

```
VoxLog/
├── index.html        ← The entire application
├── README.md         ← You are here
└── voxlog.db         ← Your saved session (generated, not committed)
```

---

## 🌐 Live App

**[lanceterrill.github.io/VoxLog](https://lanceterrill.github.io/VoxLog)**

---


