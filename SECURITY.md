# 🔒 VoxLog — Security & Compliance Documentation
### Nebraska Department of Insurance (NDOI) | NITC Policy 8-609

---

## Application Overview

**VoxLog** is a locally-hosted voicemail transcription dashboard built for internal NDOI use. It processes `.wav` voicemail recordings using locally-running AI models and stores all data on the user's workstation. No data is transmitted to external services during normal operation.

| Property | Value |
|----------|-------|
| Application Name | VoxLog |
| Version | 1.0 |
| Classification | Internal Use Only |
| Data Type | LOW IMPACT — voicemail metadata, transcription text |
| Hosting | Local workstation (127.0.0.1) |
| External Connections | None (after initial setup) |
| Compliance Framework | NITC Policy 8-609 |

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALL PROCESSING IS LOCAL                      │
│                                                                 │
│  .wav file  →  faster-whisper  →  Ollama qwen2.5  →  Browser   │
│               (127.0.0.1:5001)   (127.0.0.1:11434)             │
│                                                                 │
│  Browser  →  JSON backup file  →  Local disk only              │
│                                                                 │
│  Browser  →  CSV export  →  Local disk only                    │
│                                                                 │
│  Browser  →  Push to List  →  DOI.SHIP@nebraska.gov            │
│                               (internal GovCloud email only)    │
└─────────────────────────────────────────────────────────────────┘
```

**No audio, transcription text, or caller data is ever sent to an external server.**

---

## Components & External Dependency Analysis

| Component | Type | External? | Notes |
|-----------|------|-----------|-------|
| `index.html` | Browser UI | ❌ No | Single HTML file, no CDN calls |
| `whisper_server.py` | Python/Flask | ❌ No | Runs on 127.0.0.1:5001 |
| faster-whisper | Python library | ❌ No | Runs fully on local CPU |
| Ollama | Local LLM runtime | ❌ No | Runs on 127.0.0.1:11434 |
| qwen2.5 model | LLM | ❌ No | Downloaded once, runs locally |
| Whisper base model | STT model | ❌ No | Downloaded once, runs locally |
| Power Automate | List sync | ✅ Yes | GovCloud only — internal M365 tenant |
| DOI.SHIP mailbox | Email trigger | ✅ Yes | nebraska.gov — internal GovCloud |

**One-time internet access required** for initial setup only (downloading models and Python packages). All subsequent use is fully offline.

---

## NITC Policy 8-609 Compliance Assessment

### §1 — Data Classification

Voicemail data processed by VoxLog consists of:
- Caller names and phone numbers
- Voicemail transcription text
- Call timestamps and staff notes

This constitutes **LOW IMPACT** data under NITC 8-609 §1(c). No HIGH or MODERATE IMPACT data (SSNs, financial records, medical information) is processed.

### §2 — OCIO/RMC Approval

VoxLog processes all data locally on agency workstations. No data is transmitted to external AI services. The application does not connect to any public cloud AI API during operation.

**Assessment:** External AI service approval requirements under NITC 8-609 §2 do not apply. All AI processing occurs within the agency workstation boundary.

### §3 — Ethics & Bias

VoxLog uses AI for speech-to-text transcription and caller name extraction only. It does not make decisions, assessments, or recommendations about individuals. All AI output is subject to human review and correction before any action is taken.

**Assessment:** No automated decision-making. Human review required for all records before status is marked Done.

### §4 — Transparency & Disclosure

VoxLog is used to process voicemails left by callers. Callers are not currently notified that their voicemail may be transcribed by AI-assisted software.

**Recommended action:** Update the NDOI voicemail greeting to include a disclosure such as:
> *"Your message may be transcribed using AI-assisted software for internal processing purposes."*

**Assessment:** Disclosure gap identified. Remediation recommended before production use.

### §5 — Validity & Reliability

Transcription accuracy depends on audio quality and speaking clarity. All transcriptions are reviewed and edited by staff before use. The AI extraction pipeline uses a regex fallback if the LLM returns an empty or malformed result.

**Assessment:** Human-in-the-loop review required. No automated actions are taken based solely on AI output.

### §6 — Training & Accountability

VoxLog is maintained by NDOI IT. Staff using the application should be familiar with:
- How to review and correct AI transcriptions
- What data is stored and where
- The Push to List workflow and Power Automate integration

---

## Security Controls

| Control | Implementation |
|---------|---------------|
| Data at rest | JSON backup stored on local workstation only |
| Data in transit | All processing on 127.0.0.1 — no network transmission |
| Authentication | Windows workstation login (existing agency control) |
| Session management | Browser session only — no persistent credentials |
| API keys | None — no external API keys required |
| Logging | whisper_server.py logs to console only — no log files written |
| Audio retention | Audio files are not stored by the application — temp files deleted after transcription |

---

## Static Code Security Scan — ClawSecure Results

**Scan date:** April 2026
**Tool:** ClawSecure Proprietary Engine
**Overall result:** No exploitable vulnerabilities identified

### Finding: `exec\(` — CRITICAL (False Positive)

**Status: FALSE POSITIVE — Documented, no remediation required**

**Location:** Previously in `index.html` (now resolved) and in `sql-wasm.js` (now removed)

**Explanation:** The scanner flagged `exec[]` as a potentially dangerous code pattern. This finding was caused by:

1. `db.exec[]` — a method of the sql.js SQLite library used to run an in-memory SELECT query against a local browser database. This has been removed as part of a dependency reduction effort. The application now uses JSON for session save/restore, eliminating the sql.js dependency entirely.

2. `sql-wasm.js` — the sql.js WebAssembly loader contained `exec[]` in its minified source as part of standard WebAssembly glue code. This file has been removed from the application.

**Current status:** Both files have been removed. The `exec[]` pattern no longer appears anywhere in the VoxLog codebase. No shell execution, dynamic code evaluation, or operating system calls are present in any VoxLog file.

**Dangerous patterns confirmed absent:**

| Pattern | Risk | Present in VoxLog |
|---------|------|-------------------|
| Shell/process execution | Remote code execution | ❌ Not present |
| Dynamic JS evaluation | Code injection | ❌ Not present |
| OS command invocation | System compromise | ❌ Not present |
| External API calls | Data exfiltration | ❌ Not present |
| localStorage/cookie credentials | Credential theft | ❌ Not present |

---

## Incident Response

If a security concern is identified with VoxLog:

1. Stop the whisper_server.py process (`Ctrl+C` in the PowerShell window)
2. Stop the Python web server (`Ctrl+C`)
3. Contact NDOI IT — lance.terrill@nebraska.gov
4. Do not delete any files until IT has reviewed

---

## Document Control

| Field | Value |
|-------|-------|
| Author | Lance Terrill, IT Business Systems Analyst, NDOI |
| Last Updated | April 2026 |
| Review Cycle | Annual or upon significant application change |
| Distribution | NDOI IT, OCIO RMC (upon request) |

---

*Nebraska Department of Insurance — Internal Use Only*
*NITC Policy 8-609 | M365 GovCloud Tenant: usgovtexas*
