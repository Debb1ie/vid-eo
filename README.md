# 🎬 FrameForge

Personal AI video generation studio powered by the **Seedance 2.0 API** — free daily credits, no credit card required.

---

## Quick Start

```bash
# 1. Get a free API key at https://seedanceapi.org (Google login, no card)

# 2. Install dependencies
pip install flask flask-cors requests

# 3. Set your key and run
export SEEDANCE_API_KEY=your_key_here   # Windows: set SEEDANCE_API_KEY=...
python app.py

# 4. Open http://localhost:5000
```

---

## Features

- **Text-to-video** — describe any scene, get a real MP4 back
- **Image-to-video** — paste an image URL to animate it
- **3 quality tiers** — 480p (fast), 720p (balanced), 1080p (HD)
- **3 durations** — 4s, 8s, 12s
- **4 aspect ratios** — 16:9, 9:16, 1:1, 4:3
- **Live progress bar** — polls every 3 seconds automatically
- **One-click download** — saves MP4 directly from the browser
- **Session gallery** — all generations shown with hover-preview

---

## Project Structure

```
frameforge/
├── app.py            ← Flask backend (all API logic)
├── requirements.txt  ← Python dependencies
└── static/
    └── index.html    ← Frontend (served by Flask, no build step)
```

---

## Models

| Model | Quality | Notes |
|-------|---------|-------|
| Seedance 2.0 Fast | 480p | Fastest, fewest credits |
| Seedance 2.0 | 720p | Best balance ⭐ |
| Seedance 2.0 HD | 1080p | Best quality |

Credits reset every 24 hours.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Serves the frontend |
| POST | `/api/generate` | Start text-to-video → `{ task_id }` |
| POST | `/api/generate-from-image` | Animate an image → `{ task_id }` |
| GET | `/api/status/<task_id>` | Poll status → `{ status, video_url }` |
| GET | `/api/models` | List available models |

---

## Prompt Tips

- End with a camera style: `cinematic wide shot`, `slow dolly`, `aerial view`
- Add lighting: `golden hour`, `neon-lit`, `soft diffused light`
- Be specific: `a red fox walking through snow` not `an animal in winter`
- Tick **Camera Fixed** when you want the subject to move, not the camera

---

## Troubleshooting

**API shows Offline** — Flask isn't running. Check your terminal for errors.

**401 Unauthorized** — wrong or missing API key. Re-export and restart.

**429 Too Many Requests** — daily credits used up. Resets in 24h. Switch to 480p to use fewer credits.

**Stuck generating** — normal generation takes 60–90s. If over 3 minutes, just try again.
