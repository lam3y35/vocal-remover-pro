#!/usr/bin/env python3
"""
run.py — Vocal Remover Pro launcher
Usage:
    python run.py                # starts server + opens browser
    python run.py --no-browser   # server only (API mode)
    python run.py --port 8080    # custom port
"""

import argparse
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT    = Path(__file__).parent
BACKEND = ROOT / "backend" / "main.py"


def check_deps():
    missing = []
    for pkg in ["fastapi", "uvicorn", "torch", "torchaudio",
                "soundfile", "librosa", "numpy", "psutil"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"\n⚠  Missing packages: {', '.join(missing)}")
        print("   Run:  pip install -r requirements.txt\n")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7070)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    check_deps()

    url = f"http://{args.host}:{args.port}"
    print(f"\n🎙  Vocal Remover Pro")
    print(f"   Server  → {url}")
    print(f"   API     → {url}/docs")
    print(f"   Press Ctrl+C to stop\n")

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app",
         "--host", args.host, "--port", str(args.port), "--reload"],
        cwd=str(ROOT / "backend"),
    )

    if not args.no_browser:
        time.sleep(2)
        webbrowser.open(url)

    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        print("\n✓  Server stopped.")


if __name__ == "__main__":
    main()
