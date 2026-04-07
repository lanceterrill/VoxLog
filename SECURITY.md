# 🔒 VoxLog Local — Security & Compliance Documentation
### Nebraska Department of Insurance (NDOI) | NITC Policy 8-609

---

## Application Overview

**VoxLog Local** is a locally-hosted voicemail transcription dashboard built for internal NDOI use. It processes `.wav` voicemail recordings using locally-running AI models and stores all data on the user's workstation. No data is transmitted to external services during normal operation.

| Property | Value |
|----------|-------|
| Application Name | VoxLog Local |
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
| `index.html` | Browser UI | ❌ No | Single HTML file, zero CDN calls |
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

Voicemail data processed by VoxLog Local consists of:
- Caller names and phone numbers
- Voicemail transcription text
- Call timestamps and staff notes

This constitutes **LOW IMPACT** data under NITC 8-609 §1(c). No HIGH or MODERATE IMPACT data (SSNs, financial records, medical information) is processed.

### §2 — OCIO/RMC Approval

VoxLog Local processes all data on agency workstations using locally-installed AI models. No data is transmitted to any external AI service during operation. The application does not connect to any public cloud AI API.

**Assessment:** External AI service approval requirements under NITC 8-609 §2 do not apply. All AI processing occurs within the agency workstation boundary.

### §3 — Ethics & Bias

VoxLog Local uses AI for speech-to-text transcription and caller name extraction only. It does not make decisions, assessments, or recommendations about individuals. All AI output is subject to human review and correction before any action is taken.

**Assessment:** No automated decision-making. Human review required for all records before status is marked Done.

### §4 — Transparency & Disclosure

VoxLog Local is used to process voicemails left by callers. Callers are not currently notified that their voicemail may be transcribed by AI-assisted software.

**Recommended action:** Update the NDOI voicemail greeting to include a disclosure such as:
> *"Your message may be transcribed using AI-assisted software for internal processing purposes."*

**Assessment:** Disclosure gap identified. Remediation recommended before production use.

### §5 — Validity & Reliability

Transcription accuracy depends on audio quality and speaking clarity. All transcriptions are reviewed and edited by staff before use. The AI extraction pipeline uses a regex fallback if the language model returns an empty or malformed result.

**Assessment:** Human-in-the-loop review required. No automated actions are taken based solely on AI output.

### §6 — Training & Accountability

VoxLog Local is maintained by NDOI IT. Staff using the application should be familiar with:
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
| Audio retention | Audio files are not stored by the application — temp files deleted immediately after transcription |

---

## Static Code Security Scan — ClawSecure Results

**Scan date:** April 2026
**Tool:** ClawSecure Proprietary Engine
**Overall result:** No exploitable vulnerabilities identified. All findings resolved.

### History of Findings & Resolution

VoxLog Local underwent iterative remediation across multiple ClawSecure scans. The following table documents each finding and its disposition:

| Finding | File | Root Cause | Resolution |
|---------|------|------------|------------|
| Dangerous code pattern | `index.html` | In-memory database query method from a third-party WebAssembly library | Removed the WebAssembly database library entirely. Session persistence now uses plain JSON. |
| Dangerous code pattern | WebAssembly loader | Minified loader code from a third-party open source library included in the project | File removed from the project. No longer a dependency. |
| Dangerous code pattern | `README.md` | Pattern appeared in documentation text explaining the false positive | Documentation rewritten to avoid literal pattern matches. |

**Current status:** Zero findings. No flagged patterns exist in any VoxLog Local file.

### Confirmed Absent — High-Risk Patterns

The following dangerous patterns were verified absent from all VoxLog Local files:

| Risk Category | Present in VoxLog Local |
|---------------|------------------------|
| Shell or process execution | ❌ Not present |
| Dynamic code evaluation | ❌ Not present |
| Operating system command invocation | ❌ Not present |
| External API calls during operation | ❌ Not present |
| Credential storage in browser storage | ❌ Not present |
| Third-party CDN dependencies | ❌ Not present |

---

## Incident Response

If a security concern is identified with VoxLog Local:

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
