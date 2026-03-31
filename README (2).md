# VoxLog — Voicemail Transcription Dashboard

A single-file HTML tool for transcribing, reviewing, and syncing voicemail records to a Microsoft List via Power Automate. Built for the Nebraska Department of Insurance (NDOI).

---

## Features

- **Batch transcription** — drop `.wav` files, transcribe all at once via Groq Whisper
- **AI metadata extraction** — caller name, phone number, and call date auto-filled from transcript
- **Editable dashboard** — all fields editable inline; date/time pickers for call and return timestamps
- **Status tracking** — Pending, In Progress, Review, Done, Unreachable
- **SQLite backup/restore** — save and reload sessions as `.db` files
- **CSV export** — full export for spreadsheet analysis
- **Push to List** — sync records to a Microsoft List via email + Power Automate (no premium connectors required)

---

## Columns

Mirrors the VoxLog Microsoft List schema exactly:

| Column | Auto-filled | Editable |
|--------|-------------|----------|
| Phone Number | ✓ from transcript | ✓ |
| Caller Name | ✓ from transcript | ✓ |
| Call Date | ✓ at transcription | ✓ (date picker) |
| Call Time | ✓ at transcription | ✓ (time picker) |
| Filename | — | ✓ |
| Transcription | ✓ via Whisper | ✓ |
| Staff Name | — | ✓ |
| Returned Date | — | ✓ (date picker) |
| Returned Time | — | ✓ (time picker) |
| Notes | — | ✓ |
| Status | — | ✓ (dropdown) |

---

## Setup

### 1. Groq API Key
VoxLog uses [Groq](https://console.groq.com) for free Whisper transcription.

1. Sign up at **console.groq.com**
2. Go to **API Keys** and create a new key (starts with `gsk_`)
3. Enter it in the VoxLog key modal on load — stored in memory only, never saved to disk

### 2. Power Automate Flow (Push to List)
The Push to List feature requires a Power Automate cloud flow using standard connectors only.

**Trigger:** When a new email arrives in a shared mailbox (V2)
- Mailbox: `DOI.SHIP@nebraska.gov`
- Subject Filter: `VoxLog List Sync`
- Include Attachments: Yes

**Actions:**
1. **Compose** — `base64ToString(triggerOutputs()?['body/attachments'][0]['contentBytes'])`
2. **Parse JSON** — Content: Compose output; Schema: flat array of VoxLog fields
3. **Apply to each** — iterate Parse JSON body
4. **Create item** — SharePoint → VoxLog List, map all 11 fields
   ```
   items('Apply_to_each')?['FieldName']
   ```

**VoxLog List columns** (all Single line of text except Status which is a Choice):

`CallerName, PhoneNumber, CallDate, CallTime, Transcription, StaffName, ReturnedCallDate, ReturnedCallTime, Notes, OriginalFilename, Status`

---

## Usage

### Transcribe Voicemails
1. Click **📁 Load WAV Files** or drag `.wav` files onto the drop zone
2. Click **⚡ Transcribe All** — Groq Whisper processes each file
3. Review and edit any auto-filled fields as needed

### Save & Restore
- **💾 Backup** — downloads `voxlog.db` (SQLite) with all records
- **📂 Load Backup** — restores a saved session; new files can be added on top

### Push to Microsoft List
1. Click **📤 Push to List** — downloads a JSON file of unpushed records
2. Click **✉️ Open Outlook Email** — Outlook opens pre-addressed to `DOI.SHIP@nebraska.gov`
3. Confirm **From** is your personal account, not the shared mailbox
4. Attach the JSON file and send
5. Power Automate creates List items within ~1 minute
6. Pushed records show a green **✓** in the Actions column

---

## Technical Notes

- Single-file HTML — no build steps, no dependencies to install
- Uses [sql.js](https://github.com/sql-js/sql-js) (CDN) for SQLite in the browser
- Uses [Groq API](https://console.groq.com/docs/openai) for Whisper transcription and LLaMA metadata extraction
- API key is session-only — never written to disk or localStorage
- `.db` backup format is standard SQLite — openable in DB Browser for SQLite or any SQLite tool
- Power Automate flow uses standard M365 connectors only (no premium, no HTTP action)

---

## Environment

Built for the NDOI / OCIO M365 GovCloud environment (`stateofne.sharepoint.com`).  
Power Automate tenant: `usgovtexas` region.

---

*VoxLog is an internal NDOI tool. Not for public use.*
