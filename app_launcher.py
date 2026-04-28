#!/usr/bin/env python3
"""
app_launcher.py
Desktop entrypoint for packaged Vocal Remover Pro.
Starts FastAPI app and opens browser automatically.
"""

import sys
import threading
import time
import webbrowser
from pathlib import Path

import uvicorn


def _resolve_backend_dir() -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    candidate = base / "backend"
    return candidate if candidate.exists() else base


def main() -> None:
    backend_dir = _resolve_backend_dir()
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    # Import after path setup so frozen/unfrozen both work.
    from main import app

    host = "127.0.0.1"
    port = 7070
    url = f"http://{host}:{port}"

    def _open_browser_delayed():
        time.sleep(2.0)
        webbrowser.open(url)

    threading.Thread(target=_open_browser_delayed, daemon=True).start()
    uvicorn.run(app, host=host, port=port, reload=False, log_level="info")


if __name__ == "__main__":
    main()
