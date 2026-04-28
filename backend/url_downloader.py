#!/usr/bin/env python3
"""
backend/url_downloader.py — URL download utility using yt-dlp
Handles downloading audio from YouTube and other supported sites.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import asyncio


# Try to import yt_dlp
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False


def download_audio_from_url(
    url: str,
    output_dir: Path,
    progress_callback=None,
) -> Tuple[Optional[Path], Optional[str]]:
    """
    Download audio from a URL (YouTube, etc.).
    
    Args:
        url: The URL to download from
        output_dir: Directory to save the downloaded file
        progress_callback: Optional callback for progress updates
        
    Returns:
        Tuple of (file_path, error_message)
    """
    if not YT_DLP_AVAILABLE:
        return None, "yt-dlp is not installed. Run: pip install yt-dlp"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Progress hook for yt-dlp
    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                percent = (downloaded / total) * 100
                speed = d.get('speed', 0)
                speed_str = f"{speed / 1024 / 1024:.2f} MB/s" if speed else "N/A"
                if progress_callback:
                    progress_callback(int(percent), f"Downloading... {percent:.1f}% @ {speed_str}")
        elif d['status'] == 'finished':
            if progress_callback:
                progress_callback(90, "Download complete, processing...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Get the downloaded file path
            filename = ydl.prepare_filename(info)
            # Change extension to wav (since we're extracting audio)
            wav_path = Path(filename).with_suffix('.wav')
            
            # If the wav file exists, return it
            if wav_path.exists():
                return wav_path, None
            
            # Otherwise, look for the original file
            original_path = Path(filename)
            if original_path.exists():
                return original_path, None
            
            return None, "Downloaded file not found"
            
    except Exception as e:
        return None, f"Download failed: {str(e)}"


async def download_audio_async(
    url: str,
    output_dir: Path,
    progress_callback=None,
) -> Tuple[Optional[Path], Optional[str]]:
    """
    Async wrapper for download_audio_from_url.
    
    Args:
        url: The URL to download from
        output_dir: Directory to save the downloaded file
        progress_callback: Optional async callback for progress updates
        
    Returns:
        Tuple of (file_path, error_message)
    """
    loop = asyncio.get_event_loop()
    
    # Convert async callback to sync for yt-dlp
    def sync_progress_callback(percent: int, message: str):
        if progress_callback:
            asyncio.run_coroutine_threadsafe(
                progress_callback(percent, message),
                loop
            )
    
    return await loop.run_in_executor(
        None,
        lambda: download_audio_from_url(url, output_dir, sync_progress_callback)
    )


if __name__ == "__main__":
    # Test the downloader
    print("URL Downloader Test")
    print(f"yt-dlp available: {YT_DLP_AVAILABLE}")
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output_dir = Path("./downloads")
        
        print(f"Downloading from: {url}")
        file_path, error = download_audio_from_url(url, output_dir)
        
        if file_path:
            print(f"Downloaded successfully: {file_path}")
        else:
            print(f"Error: {error}")
