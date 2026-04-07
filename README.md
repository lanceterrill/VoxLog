# 📞 VoxLog
### *Voicemail Transcription Dashboard — Local AI Edition*

> **Drop it. Transcribe it. Push it.** — A fully offline voicemail transcription tool that turns raw `.wav` recordings into structured, searchable, actionable records — synced to Microsoft Lists via Power Automate. No internet required. No data leaves your machine.

![Version](https://img.shields.io/badge/version-1.0-00c896?style=flat-square&logo=github)
![License](https://img.shields.io/badge/license-MIT-0099ff?style=flat-square)
![Built With](https://img.shields.io/badge/built%20with-HTML%20%2F%20JS%20%2F%20Python-ffaa00?style=flat-square)
![Powered By](https://img.shields.io/badge/powered%20by-faster--whisper%20%2B%20Ollama-00c896?style=flat-square)
![Offline](https://img.shields.io/badge/fully-offline-ff4455?style=flat-square)

---

## ✨ What It Does

```
┌─────────────────────────────────────────────────────────────┐
│                        VOXLOG FLOW                          │
│                                                             │
│  .wav files  -->  Whisper (local)  -->  Dashboard           │
│                                                             │
│  Dashboard   -->  Push to List  -->  Email                  │
│                                                             │
│  Email  -->  Power Automate  -->  MS List                   │
│                          |                                  │
│                          +--> ListSync/Processed (archive)  │
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
| 💾 **JSON Backup** | Save and reload full sessions as `.json` files |
| 📊 **CSV Export** | Full export for Excel analysis |
| 📤 **Push to MS List** | One-click sync to Microsoft List via Power Automate |
| ✅ **Pushed Flag** | Green ✓ tracks which records have been synced |
| 🔍 **Search & Sort** | Full-text search across all columns, multi-column sort |
| 🌙 **Dark / Light Mode** | Persistent theme toggle |
| 🔒 **Fully Offline** | No data leaves your machine — 100% local AI |

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
│  🎙️ WAV Files  →  faster-whisper  →  Ollama qwen2.5 metadata    │
│                   (127.0.0.1:5001)    (127.0.0.1:11434)          │
│                                                                  │
│  📋 VoxLog Dashboard  →  ✏️ Staff Review & Edit  →  📤 Push     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📁 Folder Structure

```
VoxLog/
├── index.html           ← The entire application (open this)
├── whisper_server.py    ← Local transcription server (run this first)
├── config.json          ← App configuration reference
├── README.md            ← You are here
├── SECURITY.md          ← Security & compliance documentation
└── files/               ← Your voicemail .wav files go here
```

---

## 🛠️ Technical Stack

```
┌─────────────────────────────────────────────────────┐
│  🌐 Frontend    │  Vanilla HTML / CSS / JS           │
│  🗄️ Storage     │  JSON backup (local file)          │
│  🎙️ Transcribe  │  faster-whisper (local, CPU)       │
│  🧠 Metadata    │  Ollama qwen2.5 (local)            │
│  🔄 Sync        │  Power Automate (standard only)    │
│  🔒 Privacy     │  100% offline — no external calls  │
└─────────────────────────────────────────────────────┘
```

**Zero external dependencies.** Everything runs in the browser or on localhost.

---

## 🔐 Security Scan Notes — False Positive Documentation

> See **SECURITY.md** for the full compliance and RMC documentation.

ClawSecure previously flagged dangerous code patterns in the codebase. Both sources have been eliminated:

- The WebAssembly database library has been removed entirely. VoxLog no longer uses it.
- The associated query call has been removed. Session save/restore now uses plain JSON.

No flagged patterns remain in any VoxLog file. See SECURITY.md for the full finding disposition.

---

---

# 🛠️ ADMIN GUIDE

> For IT staff responsible for setting up and maintaining VoxLog on a workstation.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.10+ | Installed via Microsoft Store or python.org |
| Ollama | [ollama.com](https://ollama.com) — install and pull `qwen2.5` |
| `qwen2.5:latest` model | Run `ollama pull qwen2.5` after installing Ollama |
| Modern browser | Edge, Chrome, or Firefox |

---

## One-Time Setup

### 1. Install Python dependencies

Open PowerShell and run:

```powershell
pip install faster-whisper flask flask-cors
```

faster-whisper will download the Whisper `base` model (~150MB) automatically on first run.

### 2. Install Ollama and pull the model

Download Ollama from [ollama.com](https://ollama.com), install it, then run:

```powershell
ollama pull qwen2.5
```

---

## Starting VoxLog (Every Session)

VoxLog requires **three services running** before opening the browser. Open three separate PowerShell windows:

**Window 1 — Whisper transcription server:**
```powershell
cd "C:\path\to\VoxLog"
python whisper_server.py
```
Wait for: `Model ready. Serving on http://127.0.0.1:5001`

**Window 2 — Ollama (caller extraction):**
```powershell
ollama serve
```
Wait for: `Listening on 127.0.0.1:11434`

**Window 3 — Web server:**
```powershell
cd "C:\path\to\VoxLog"
python -m http.server 8080
```

Then open your browser to: **`http://127.0.0.1:8080`**

Click **Connect & Continue →** in the startup modal.

---

## Whisper Model Options

Edit `whisper_server.py` and change `MODEL_SIZE` at the top of the file:

| Model | Speed | Accuracy | Download Size |
|-------|-------|----------|---------------|
| `tiny` | Fastest | Lower | ~75MB |
| `base` | Fast | Good ✅ *default* | ~150MB |
| `small` | Moderate | Better | ~480MB |
| `medium` | Slow | Best CPU option | ~1.5GB |

```python
MODEL_SIZE = "base"   # change this line
```

---

## Power Automate List Sync

The Push to List feature exports a JSON file and opens an Outlook email. The receiving Power Automate flow (standard connectors only) handles the rest.

- **Trigger email:** `DOI.SHIP@nebraska.gov`
- **Subject must be exactly:** `VoxLog List Sync`
- **Flow:** Shared Mailbox V2 trigger → Parse JSON → Apply to each → Create item in VoxLog MS List

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Cannot reach Whisper server" | Run `python whisper_server.py` in its own PowerShell window |
| "Cannot reach Ollama" | Run `ollama serve` in a separate PowerShell window |
| Browser shows old version | Hard refresh with `Ctrl+Shift+R` |
| `localhost:8080` not loading | Use `http://127.0.0.1:8080` instead |
| Transcription is slow | Switch `MODEL_SIZE` to `tiny` in `whisper_server.py` |
| ClawSecure scan findings | All resolved — see SECURITY.md |

---

## Security & Compliance

- 🔒 All audio processed **locally** — no data sent to external APIs
- 🏛️ No OCIO/RMC approval required for external AI — fully on-premise
- 📋 Transcription data stays in your browser and local `.json` backup file only
- 🗑️ Backup files should be treated as records per your agency retention schedule
- 📄 See **SECURITY.md** for full NITC 8-609 assessment and scan documentation

---

---

# 👤 USER GUIDE

> For NDOI staff using VoxLog day-to-day to process voicemails.

---

## Getting Started

VoxLog runs in your browser. Your IT admin will have it set up and running — just open:

```
http://127.0.0.1:8080
```

When the **Local AI Setup** modal appears, click **Connect & Continue →**. If you get an error, contact IT — the background services may not be started yet.

> 💡 Use **Demo Mode** (Skip button) to explore the dashboard with sample data before processing real voicemails.

---

## Loading Voicemails

1. Click **📁 Load WAV Files** in the toolbar
2. Navigate to your voicemail folder and select one or multiple `.wav` files
3. Or drag and drop files directly onto the drop zone
4. Files appear in the dashboard immediately — you can add more at any time

---

## Transcribing

1. Click **⚡ Transcribe All** to process every loaded file at once
2. Or click the **⚡** button on an individual row to transcribe just that one
3. A progress bar shows how many files have been processed
4. When complete, each row will show the full transcription, caller name, phone number, and call date — all auto-filled

> ⏱️ Transcription runs locally — a typical 1-minute voicemail takes about 10–20 seconds.

---

## Reviewing & Editing

Every column in the table is editable — just click on any cell:

| Column | How to Edit |
|--------|-------------|
| 📞 Phone Number | Click and type |
| 👤 Caller Name | Click and type |
| 📅 Call Date | Click the date picker |
| 🕐 Call Time | Click the time picker |
| 📝 Transcription | Click and edit the text |
| 👷 Staff Name | Type your name |
| 📅 Returned Date | Click the date picker when callback is made |
| 🕐 Returned Time | Click the time picker |
| 🗒️ Notes | Click and type any notes |
| 🔵 Status | Click to cycle through status values |

---

## Status Values

| Status | Meaning |
|--------|---------|
| 🔵 **Pending** | New — not yet handled |
| 🟡 **In Progress** | Being worked on |
| 🩷 **Review** | Needs supervisor review |
| 🟢 **Done** | Callback completed |
| 🔴 **Unreachable** | Could not reach the caller |

---

## Searching & Sorting

- **Search bar** — type anything to filter across all columns in real time
- **Sort dropdown** — sort by phone number (default), date, caller name, filename, or status

---

## Saving Your Work

Click **💾 Backup** to save everything to a `voxlog-backup.json` file. Reload it next session with **📂 Load Backup**.

> 💡 Save regularly — your session is lost if you close the browser without saving.

---

## Pushing to Microsoft List

1. Click **📤 Push to List**
2. A JSON file downloads automatically
3. An Outlook email draft opens — attach the downloaded JSON file
4. Send the email — Power Automate handles the rest
5. Pushed records show a green **✓** in the dashboard

> 📧 Do not change the email subject line — Power Automate uses it as a trigger.

---

## Exporting to Excel

Click **⬇ Export CSV** to download all records as a `.csv` file that opens directly in Excel.

---

## Tips

- You can load more files at any time, even after transcribing others
- Duplicate files (same size and date) are automatically skipped
- If a transcription looks wrong, click the cell and correct it manually
- Dark/light mode toggle is in the top-right corner (🌙 / ☀️)
- The search bar filters in real time — no need to press Enter

---

## Need Help?

Contact your IT department or refer to the Admin Guide section of this README.

---

*VoxLog — Built for the Nebraska Department of Insurance (NDOI)*
*Power Automate tenant: `usgovtexas` · SharePoint: `stateofne.sharepoint.com/sites/DOI.SHIP`*
