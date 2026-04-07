"""
whisper_server.py — VoxLog Local Transcription Server
Runs faster-whisper locally and exposes a simple HTTP API for VoxLog.

Usage:
    pip install faster-whisper flask
    python whisper_server.py

Endpoints:
    GET  /health       — status check
    POST /transcribe   — accepts multipart form with 'file' (.wav)
                         returns {"text": "..."}

Model: 'base' by default (good speed/accuracy balance on CPU).
Change MODEL_SIZE below to 'tiny' (fastest) or 'small' (more accurate).
"""

import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from faster_whisper import WhisperModel

# ── CONFIG ────────────────────────────────────────────────────────────────────
MODEL_SIZE = "base"       # tiny | base | small | medium | large-v2
DEVICE     = "cpu"        # cpu (always works) | cuda (if you have a GPU + CUDA)
COMPUTE    = "int8"       # int8 is fastest on CPU
PORT       = 5001
# ─────────────────────────────────────────────────────────────────────────────

print(f"[VoxLog Whisper] Loading model '{MODEL_SIZE}' on {DEVICE}...")
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE)
print(f"[VoxLog Whisper] Model ready. Serving on http://localhost:{PORT}")

app = Flask(__name__)
CORS(app)  # Allow requests from the browser (localhost:8080)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": MODEL_SIZE, "device": DEVICE})


@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files["file"]
    if not audio_file.filename:
        return jsonify({"error": "Empty filename"}), 400

    # Save to a temp file — faster-whisper needs a file path
    suffix = os.path.splitext(audio_file.filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        segments, info = model.transcribe(tmp_path, beam_size=5)
        text = " ".join(seg.text.strip() for seg in segments).strip()
        if not text:
            text = "[No speech detected]"
        print(f"[VoxLog Whisper] Transcribed: {audio_file.filename} → {text[:80]}...")
        return jsonify({"text": text, "language": info.language})
    except Exception as e:
        print(f"[VoxLog Whisper] Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=False)
