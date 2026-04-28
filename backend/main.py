#!/usr/bin/env python3
"""
backend/main.py — FastAPI server for Vocal Remover Pro
All API endpoints for file upload, URL processing, progress streaming, and job management.
"""

import os
import sys
import json
import uuid
import shutil
import asyncio
import threading
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import psutil

# Add backend to path for engine import
sys.path.insert(0, str(Path(__file__).parent))

app = FastAPI(title="Vocal Remover Pro API", version="1.0.0")

# Enable CORS for all origins (for local dev and PWA)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
ROOT = Path(__file__).parent.parent
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

CONFIG_PATH = Path.home() / ".vocal_remover_pro_config.json"
JOBS: Dict[str, Dict[str, Any]] = {}  # job_id -> job info
MODEL_CACHE = None

# Default config
DEFAULT_CONFIG = {
    "model_name": "htdemucs_ft",
    "segment": 8.0,
    "overlap": 1.0,
    "shifts": 3,
    "output_format": "wav",
    "output_all_stems": False,
    "device": "auto",
    "audio_bitrate": "256k",
    "adaptive_mode": True,
    "long_file_mode": "auto",
    "chunk_minutes": 10,
    "update_manifest_url": "",
}


def load_config() -> Dict[str, Any]:
    """Load configuration from disk or return defaults."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Merge with defaults for missing keys
                return {**DEFAULT_CONFIG, **config}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration to disk."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False


def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    """Get job info by ID."""
    return JOBS.get(job_id)


def create_job(task_type: str, source: str, config: Dict[str, Any]) -> str:
    """Create a new job entry."""
    job_id = str(uuid.uuid4())[:8]
    JOBS[job_id] = {
        "id": job_id,
        "task_type": task_type,  # "file" or "url"
        "source": source,
        "config": config,
        "status": "pending",  # pending, running, completed, failed, cancelled
        "progress": 0,
        "message": "Waiting to start...",
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "output_files": [],
        "error": None,
    }
    return job_id


def update_job(job_id: str, **kwargs):
    """Update job fields."""
    if job_id in JOBS:
        JOBS[job_id].update(kwargs)


async def run_separation_engine(job_id: str, file_path: Optional[Path] = None, url: Optional[str] = None):
    """Run the actual separation process (placeholder - integrates with engine.py)."""
    job = get_job(job_id)
    if not job:
        return
    
    try:
        update_job(job_id, status="running", message="Loading model...")
        
        # Simulate separation process (replace with actual engine call)
        # In production, this would call engine.py's separate function
        await asyncio.sleep(0.5)
        update_job(job_id, progress=20, message="Processing audio...")
        
        await asyncio.sleep(0.5)
        update_job(job_id, progress=50, message="Separating vocals...")
        
        await asyncio.sleep(0.5)
        update_job(job_id, progress=80, message="Generating output files...")
        
        await asyncio.sleep(0.3)
        
        # Create dummy output files for demonstration
        output_dir = OUTPUTS_DIR / job_id
        output_dir.mkdir(exist_ok=True)
        
        vocals_path = output_dir / "vocals.wav"
        instrumental_path = output_dir / "instrumental.wav"
        
        # If we have an input file, copy it as placeholder; otherwise create empty
        if file_path and file_path.exists():
            shutil.copy(file_path, vocals_path)
            shutil.copy(file_path, instrumental_path)
        else:
            vocals_path.touch()
            instrumental_path.touch()
        
        update_job(
            job_id,
            status="completed",
            progress=100,
            message="Done!",
            completed_at=datetime.now().isoformat(),
            output_files=[str(vocals_path), str(instrumental_path)],
        )
        
    except Exception as e:
        update_job(
            job_id,
            status="failed",
            message=f"Error: {str(e)}",
            error=str(e),
            completed_at=datetime.now().isoformat(),
        )


@app.get("/")
async def root():
    """Serve the frontend index.html."""
    frontend_index = ROOT / "frontend" / "index.html"
    if frontend_index.exists():
        return FileResponse(frontend_index, media_type="text/html")
    return {"message": "Vocal Remover Pro API is running. Visit /docs for API documentation."}


@app.post("/api/separate")
async def separate_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    config_json: Optional[str] = Form(None),
):
    """Upload a file for vocal separation."""
    config = json.loads(config_json) if config_json else load_config()
    
    # Save uploaded file temporarily
    temp_dir = OUTPUTS_DIR / "temp"
    temp_dir.mkdir(exist_ok=True)
    temp_file = temp_dir / f"{uuid.uuid4()}_{file.filename}"
    
    try:
        with open(temp_file, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    job_id = create_job("file", file.filename, config)
    
    # Start processing in background
    background_tasks.add_task(run_separation_engine, job_id, temp_file)
    
    return {"job_id": job_id, "status": "pending", "message": "File uploaded successfully"}


@app.post("/api/separate-url")
async def separate_url(
    background_tasks: BackgroundTasks,
    url: str = Form(...),
    config_json: Optional[str] = Form(None),
):
    """Process a URL (YouTube, etc.) for vocal separation."""
    config = json.loads(config_json) if config_json else load_config()
    
    job_id = create_job("url", url, config)
    
    # Start processing in background
    background_tasks.add_task(run_separation_engine, job_id, None, url)
    
    return {"job_id": job_id, "status": "pending", "message": "URL submitted for processing"}


@app.get("/api/progress/{job_id}")
async def stream_progress(job_id: str):
    """Server-Sent Events stream for real-time progress updates."""
    
    async def generate():
        last_progress = -1
        while True:
            job = get_job(job_id)
            if not job:
                yield f"data: {json.dumps({'error': 'Job not found'})}\n\n"
                return
            
            # Only send if progress changed
            if job["progress"] != last_progress:
                last_progress = job["progress"]
                yield f"data: {json.dumps(job)}\n\n"
            
            # Stop streaming if job is complete/failed/cancelled
            if job["status"] in ["completed", "failed", "cancelled"]:
                yield f"data: {json.dumps(job)}\n\n"
                return
            
            await asyncio.sleep(0.3)
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@app.get("/api/job/{job_id}")
async def get_job_status(job_id: str):
    """Get job status as JSON."""
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.delete("/api/job/{job_id}")
async def cancel_job(job_id: str):
    """Cancel a job and clean up resources."""
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job["status"] in ["completed", "failed", "cancelled"]:
        # Just cleanup, don't change status
        pass
    else:
        update_job(job_id, status="cancelled", message="Cancelled by user")
    
    # Cleanup files
    output_dir = OUTPUTS_DIR / job_id
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    # Remove from jobs dict after delay (or keep for history)
    # For now, just mark as cancelled
    
    return {"status": "cancelled", "job_id": job_id}


@app.post("/api/cancel/{job_id}")
async def cancel_job_post(job_id: str):
    """Alternative POST endpoint to cancel a job."""
    return await cancel_job(job_id)


@app.get("/api/download/{job_id}")
async def download_vocals(job_id: str):
    """Download the separated vocals file."""
    job = get_job(job_id)
    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Job not found or not completed")
    
    if not job["output_files"]:
        raise HTTPException(status_code=404, detail="No output files found")
    
    # Return first file (vocals)
    vocals_path = Path(job["output_files"][0])
    if not vocals_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        vocals_path,
        media_type="audio/wav",
        filename=f"vocals_{job_id}.wav",
    )


@app.get("/api/stems/{job_id}/{stem}")
async def download_stem(job_id: str, stem: str):
    """Download a specific stem (vocals, drums, bass, other)."""
    job = get_job(job_id)
    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Job not found or not completed")
    
    output_dir = OUTPUTS_DIR / job_id
    stem_path = output_dir / f"{stem}.wav"
    
    if not stem_path.exists():
        raise HTTPException(status_code=404, detail=f"Stem '{stem}' not found")
    
    return FileResponse(stem_path, media_type="audio/wav", filename=f"{stem}_{job_id}.wav")


@app.get("/api/config")
async def get_config_endpoint():
    """Get current configuration."""
    return load_config()


@app.post("/api/config")
async def save_config_endpoint(config: Dict[str, Any]):
    """Save configuration to disk."""
    if save_config(config):
        return {"status": "success", "message": "Configuration saved"}
    raise HTTPException(status_code=500, detail="Failed to save configuration")


@app.get("/api/system")
async def get_system_info():
    """Get system information (GPU, RAM, ffmpeg)."""
    import subprocess
    
    # Check for CUDA
    cuda_available = False
    try:
        import torch
        cuda_available = torch.cuda.is_available()
    except ImportError:
        pass
    
    # Check for ffmpeg
    ffmpeg_exists = shutil.which("ffmpeg") is not None
    
    # Get RAM info
    ram = psutil.virtual_memory()
    
    return {
        "cuda_available": cuda_available,
        "ffmpeg_installed": ffmpeg_exists,
        "ram_total_gb": round(ram.total / (1024**3), 2),
        "ram_available_gb": round(ram.available / (1024**3), 2),
        "cpu_count": psutil.cpu_count(logical=False),
        "platform": sys.platform,
    }


@app.get("/api/update/check")
async def check_update():
    """Check for updates using manifest URL."""
    config = load_config()
    manifest_url = config.get("update_manifest_url", "")
    
    if not manifest_url:
        return {"update_available": False, "message": "No update manifest configured"}
    
    # In production, fetch and compare versions
    return {"update_available": False, "message": "You are on the latest version"}


@app.get("/api/diagnostics")
async def get_diagnostics():
    """Export diagnostics payload for support/AI assistance."""
    config = load_config()
    system_info = await get_system_info()
    
    return {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "config": config,
        "system": system_info,
        "active_jobs": len([j for j in JOBS.values() if j["status"] in ["pending", "running"]]),
        "outputs_dir": str(OUTPUTS_DIR),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7070)
