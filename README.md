# 🎙 Vocal Remover Pro

Studio-grade vocal separation with a beautiful web UI.  
Backend: **FastAPI + PyTorch (Demucs)** · Frontend: **HTML/CSS/JS (pure, no build step)**

---

## 📁 Project Structure

```
vocal-remover-pro/
├── backend/
│   ├── main.py        ← FastAPI server (all API endpoints)
│   └── engine.py      ← Separation engine (PyTorch / torchaudio)
├── frontend/
│   └── index.html     ← Full SPA (drag-drop, SSE progress, settings)
├── outputs/           ← Created automatically on first run
├── run.py             ← One-click launcher
├── build.py           ← Package as .exe
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start (Dev Mode)

### 1. Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | ≥ 3.10 | python.org |
| ffmpeg | any | ffmpeg.org → add to PATH |
| CUDA (optional) | 11.8 / 12.x | For GPU acceleration |

### 2. Install Python dependencies

```bash
# CPU-only (works anywhere)
pip install -r requirements.txt

# GPU (CUDA 11.8) — much faster
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

### 3. Run

```bash
python run.py
```

This will:
- Start the FastAPI server on **http://127.0.0.1:7070**
- Open your browser automatically
- The API docs are at **http://127.0.0.1:7070/docs**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/separate` | Upload file → returns `job_id` |
| `POST` | `/api/separate-url` | YouTube/URL download → `job_id` |
| `GET`  | `/api/progress/{id}` | **SSE stream** — real-time progress |
| `GET`  | `/api/download/{id}` | Download separated vocals |
| `GET`  | `/api/stems/{id}/{stem}` | Download individual stem |
| `GET`  | `/api/job/{id}` | Job status (JSON) |
| `DELETE` | `/api/job/{id}` | Cancel + cleanup |
| `POST` | `/api/cancel/{id}` | Cancel running job |
| `GET`  | `/api/config` | Get current config |
| `POST` | `/api/config` | Save config to disk |
| `GET`  | `/api/system` | System info (GPU, RAM, ffmpeg) |
| `GET`  | `/api/update/check` | Check update manifest + latest version |
| `GET`  | `/api/diagnostics` | Export diagnostics payload for support/AI |

### Example (Python client)

```python
import requests, sseclient, json

BASE = "http://127.0.0.1:7070"

# 1. Upload
with open("song.mp3", "rb") as f:
    r = requests.post(f"{BASE}/api/separate",
                      files={"file": f},
                      data={"config_json": json.dumps({"model_name": "htdemucs_ft"})})
job_id = r.json()["job_id"]

# 2. Stream progress
stream = requests.get(f"{BASE}/api/progress/{job_id}", stream=True)
for line in stream.iter_lines():
    if line.startswith(b"data:"):
        ev = json.loads(line[5:])
        print(ev)
        if ev["type"] == "done":
            break

# 3. Download
r = requests.get(f"{BASE}/api/download/{job_id}")
with open("vocals.wav", "wb") as f:
    f.write(r.content)
```

---

## 🖥 Package as Desktop App (.exe / binary)

### Windows `.exe`

```bash
# Install PyInstaller first
pip install pyinstaller

# Build
python build.py
```

Output: `dist/VocalRemoverPro/VocalRemoverPro.exe`  
**Distribute the whole folder** (not just the .exe) — it contains DLLs.

Double-clicking the `.exe`:
- Starts the FastAPI server silently
- Opens the UI in your default browser automatically

### macOS `.app`

Same command — PyInstaller produces a macOS binary.  
To wrap as `.app`, add `--windowed` flag in `build.py`.

### Linux AppImage (optional)

```bash
pip install pyinstaller
python build.py
# Then wrap dist/ with appimagetool
```

---

## 📱 Mobile App (Progressive Web App — PWA)

The frontend is PWA-ready. On a local network:

1. Run the server with `python run.py --host 0.0.0.0`
2. Find your PC's local IP (e.g. `192.168.1.100`)
3. On Android/iOS, open `http://192.168.1.100:7070`
4. **Android**: Menu → "Add to Home Screen" → works like a native app
5. **iOS**: Safari Share → "Add to Home Screen"

> For full offline PWA, add a `manifest.json` and `service-worker.js` (not required for local network use).

---

## ⚙ Configuration

Settings are saved to `~/.vocal_remover_pro_config.json`.

| Key | Default | Description |
|-----|---------|-------------|
| `model_name` | `htdemucs_ft` | `htdemucs_ft` / `htdemucs` / `mdx` / `demucs` |
| `segment` | `8.0` | Chunk length in seconds |
| `overlap` | `1.0` | Overlap between chunks |
| `shifts` | `3` | Time-shift ensemble count |
| `output_format` | `wav` | `wav` / `mp3` / `flac` / `aac` / `ogg` |
| `output_all_stems` | `false` | Export drums/bass/other/vocals separately |
| `device` | `auto` | `auto` / `cuda` / `cpu` |
| `audio_bitrate` | `256k` | For lossy formats |
| `adaptive_mode` | `true` | Auto tune settings by hardware/file size |
| `long_file_mode` | `auto` | `auto` / `chunk` / `direct` |
| `chunk_minutes` | `10` | Chunk size for long processing |
| `update_manifest_url` | `""` | JSON URL for upgrade checks |

---

## 🚀 Production Deployment

```bash
# With Nginx as reverse proxy (recommended)
uvicorn backend.main:app --host 0.0.0.0 --port 7070 --workers 1

# Or with gunicorn (Linux/macOS)
gunicorn backend.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:7070
```

> **Note**: Use `--workers 1` — the model cache is not yet multi-process safe.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `ffmpeg not found` | Install ffmpeg and add to PATH. Windows: `winget install ffmpeg` |
| `CUDA out of memory` | Reduce `segment` to 4s, or switch to `mdx` model |
| `yt-dlp not installed` | `pip install yt-dlp` |
| Model download slow | Models download once from HuggingFace (~300MB each) |
| Port in use | `python run.py --port 8080` |
