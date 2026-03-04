"""
FrameForge - AI Video Generation Backend
Powered by Seedance 2.0 API (FREE daily credits, no credit card)

SETUP:
  1. Sign up free at https://seedanceapi.org  (Google login)
  2. Copy your API key from the dashboard
  3. Run:  export SEEDANCE_API_KEY=your_key_here
  4. Run:  python app.py
  5. Open:  http://localhost:5000
"""

import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
API_KEY  = os.environ.get("SEEDANCE_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://seedanceapi.org/api/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type":  "application/json",
}

# ─── SERVE FRONTEND ───────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# ─── HEALTH / MODEL LIST ──────────────────────────────────────────────────────
@app.route("/api/models")
def models():
    return jsonify({
        "models": [
            {"id": "seedance-v2-480p", "name": "Seedance 2.0 Fast", "quality": "480p", "tier": "free"},
            {"id": "seedance-v2",      "name": "Seedance 2.0",      "quality": "720p", "tier": "free"},
            {"id": "seedance-v2-hd",   "name": "Seedance 2.0 HD",   "quality": "1080p","tier": "free"},
        ]
    })

# ─── TEXT-TO-VIDEO ────────────────────────────────────────────────────────────
@app.route("/api/generate", methods=["POST"])
def generate():
    body         = request.json or {}
    prompt       = body.get("prompt", "").strip()
    duration     = int(body.get("duration", 8))
    aspect_ratio = body.get("aspect_ratio", "16:9")
    resolution   = body.get("resolution", "720p")
    camera_fixed = bool(body.get("camera_fixed", False))

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    payload = {
        "prompt":       prompt,
        "duration":     duration,
        "aspect_ratio": aspect_ratio,
        "resolution":   resolution,
        "camera_fixed": camera_fixed,
    }

    try:
        resp = requests.post(f"{BASE_URL}/videos/generate", headers=HEADERS, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        task_id = data.get("task_id") or data.get("id") or data.get("video_id")
        if not task_id:
            return jsonify({"error": "No task_id returned", "raw": data}), 500
        return jsonify({"task_id": task_id})
    except requests.HTTPError as e:
        return jsonify({"error": str(e), "details": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── IMAGE-TO-VIDEO ───────────────────────────────────────────────────────────
@app.route("/api/generate-from-image", methods=["POST"])
def generate_from_image():
    body         = request.json or {}
    prompt       = body.get("prompt", "").strip()
    image_url    = body.get("image_url", "").strip()
    duration     = int(body.get("duration", 8))
    aspect_ratio = body.get("aspect_ratio", "16:9")
    resolution   = body.get("resolution", "720p")

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    payload = {
        "prompt":       prompt,
        "image_url":    image_url,
        "duration":     duration,
        "aspect_ratio": aspect_ratio,
        "resolution":   resolution,
    }

    try:
        resp = requests.post(f"{BASE_URL}/videos/generate", headers=HEADERS, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        task_id = data.get("task_id") or data.get("id") or data.get("video_id")
        if not task_id:
            return jsonify({"error": "No task_id returned", "raw": data}), 500
        return jsonify({"task_id": task_id})
    except requests.HTTPError as e:
        return jsonify({"error": str(e), "details": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── POLL STATUS ──────────────────────────────────────────────────────────────
@app.route("/api/status/<task_id>")
def poll_status(task_id):
    try:
        resp = requests.get(f"{BASE_URL}/videos/status/{task_id}", headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        raw_status = data.get("status", "pending")
        status_map = {
            "queued": "pending", "pending": "pending",
            "processing": "processing", "generating": "processing", "running": "processing",
            "succeeded": "completed", "completed": "completed", "success": "completed",
            "failed": "failed", "error": "failed",
        }
        norm = status_map.get(raw_status, "processing")

        video_url = (
            data.get("video_url") or data.get("url")
            or (data.get("video") or {}).get("url")
            or (data.get("output") or {}).get("video_url")
        )

        return jsonify({"status": norm, "video_url": video_url, "progress": data.get("progress", 0)})
    except requests.HTTPError as e:
        return jsonify({"error": str(e)}), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\n  🎬  FrameForge running at http://localhost:5000")
    if API_KEY == "YOUR_API_KEY_HERE":
        print("  ⚠️   No API key! Get your FREE key at https://seedanceapi.org\n")
    app.run(debug=True, port=5000)
