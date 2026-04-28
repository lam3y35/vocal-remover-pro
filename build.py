#!/usr/bin/env python3
"""
build.py — Build standalone desktop package using PyInstaller.
Output:
  dist/VocalRemoverPro/VocalRemoverPro.exe (Windows)
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD_DIR = ROOT / "build"
DIST_DIR = ROOT / "dist"


def _run(cmd: list[str]) -> None:
    print("»", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True, cwd=str(ROOT))


def _data_arg(src: Path, dst: str) -> str:
    sep = ";" if sys.platform.startswith("win") else ":"
    return f"{src}{sep}{dst}"


def main() -> None:
    for folder in (BUILD_DIR, DIST_DIR):
        if folder.exists():
            shutil.rmtree(folder)
    BUILD_DIR.mkdir(exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onedir",
        "--windowed",
        "--name",
        "VocalRemoverPro",
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR / "work"),
        "--specpath",
        str(BUILD_DIR),
        "--add-data",
        _data_arg(ROOT / "backend", "backend"),
        "--add-data",
        _data_arg(ROOT / "frontend", "frontend"),
        "--hidden-import",
        "uvicorn.logging",
        "--hidden-import",
        "uvicorn.loops.auto",
        "--hidden-import",
        "uvicorn.protocols.http.auto",
        "--hidden-import",
        "uvicorn.lifespan.on",
        "--hidden-import",
        "torchaudio.pipelines",
        str(ROOT / "app_launcher.py"),
    ]
    _run(cmd)

    out_dir = DIST_DIR / "VocalRemoverPro"
    exe_name = "VocalRemoverPro.exe" if sys.platform.startswith("win") else "VocalRemoverPro"
    print("\nBuild complete.")
    print(f"Executable: {out_dir / exe_name}")
    print("Share the whole VocalRemoverPro folder (zip it), not the exe only.")
    print("Receiver still needs ffmpeg installed and added to PATH.")


if __name__ == "__main__":
    main()
