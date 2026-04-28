#!/usr/bin/env python3
"""
backend/engine.py — Separation engine using PyTorch and Demucs
Handles actual audio separation processing.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
import asyncio

# Try to import torch and torchaudio
try:
    import torch
    import torchaudio
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# Try to import demucs
try:
    from demucs import pretrained
    from demucs.apply import apply_model
    from demucs.audio import save_audio
    DEMUCS_AVAILABLE = True
except ImportError:
    DEMUCS_AVAILABLE = False

# Try to import librosa for audio processing
try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False


class SeparationEngine:
    """Main separation engine class."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.device = self._get_device()
        
    def _get_device(self) -> str:
        """Determine the best device (cuda/cpu)."""
        device_config = self.config.get('device', 'auto')
        
        if device_config == 'cuda' and TORCH_AVAILABLE and torch.cuda.is_available():
            return 'cuda'
        elif device_config == 'cpu':
            return 'cpu'
        else:
            # Auto mode
            if TORCH_AVAILABLE and torch.cuda.is_available():
                return 'cuda'
            return 'cpu'
    
    def load_model(self, model_name: Optional[str] = None):
        """Load the separation model."""
        if not DEMUCS_AVAILABLE:
            raise ImportError("Demucs is not installed. Run: pip install demucs")
        
        model_name = model_name or self.config.get('model_name', 'htdemucs_ft')
        
        try:
            self.model = pretrained.get_model(model_name)
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            raise RuntimeError(f"Failed to load model {model_name}: {str(e)}")
    
    async def separate(
        self,
        input_path: Path,
        output_dir: Path,
        progress_callback=None,
    ) -> List[Path]:
        """
        Separate audio file into stems.
        
        Args:
            input_path: Path to input audio file
            output_dir: Directory to save output files
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of paths to output files
        """
        if not self.model:
            self.load_model()
        
        if progress_callback:
            await progress_callback(10, "Loading audio...")
        
        # Load audio
        try:
            wav, sr = torchaudio.load(str(input_path))
        except Exception as e:
            raise RuntimeError(f"Failed to load audio file: {str(e)}")
        
        # Convert to stereo if needed
        if wav.shape[0] == 1:
            wav = wav.repeat(2, 1)
        
        # Resample if needed
        if self.model.samplerate != sr:
            wav = torchaudio.functional.resample(wav, sr, self.model.samplerate)
        
        if progress_callback:
            await progress_callback(20, "Preparing model...")
        
        # Get model parameters
        segment = self.config.get('segment', 8.0)
        overlap = self.config.get('overlap', 1.0)
        shifts = self.config.get('shifts', 3) if self.device == 'cuda' else 0
        
        # Apply model
        if progress_callback:
            await progress_callback(30, "Running separation...")
        
        try:
            with torch.no_grad():
                ref = wav.mean(0)
                wav = (wav - ref.mean()) / ref.std()
                
                sources = apply_model(
                    self.model,
                    wav[None].to(self.device),
                    segment=segment,
                    overlap=overlap,
                    shifts=shifts,
                )[0]
                
                sources = sources * ref.std() + ref.mean()
            
            sources = sources.cpu()
            
        except Exception as e:
            raise RuntimeError(f"Separation failed: {str(e)}")
        
        if progress_callback:
            await progress_callback(70, "Saving output files...")
        
        # Save output files
        output_dir.mkdir(parents=True, exist_ok=True)
        output_files = []
        
        stem_names = ['vocals', 'drums', 'bass', 'other']
        output_format = self.config.get('output_format', 'wav')
        
        for i, source in enumerate(sources):
            stem_name = stem_names[i] if i < len(stem_names) else f'stem_{i}'
            output_path = output_dir / f"{stem_name}.{output_format}"
            
            try:
                save_audio(source, output_path, samplerate=self.model.samplerate)
                output_files.append(output_path)
                
                if progress_callback:
                    progress = 70 + (i + 1) * 7
                    await progress_callback(progress, f"Saved {stem_name}...")
                    
            except Exception as e:
                print(f"Warning: Failed to save {stem_name}: {str(e)}")
        
        # Create combined instrumental if requested
        if len(sources) > 1:
            instrumental = sources[1:].sum(dim=0)
            instrumental_path = output_dir / f"instrumental.{output_format}"
            
            try:
                save_audio(instrumental, instrumental_path, samplerate=self.model.samplerate)
                output_files.append(instrumental_path)
            except Exception as e:
                print(f"Warning: Failed to save instrumental: {str(e)}")
        
        if progress_callback:
            await progress_callback(100, "Done!")
        
        return output_files
    
    def unload_model(self):
        """Unload model to free memory."""
        if self.model:
            del self.model
            self.model = None
            
            if TORCH_AVAILABLE and self.device == 'cuda':
                torch.cuda.empty_cache()


async def separate_file(
    input_path: Path,
    output_dir: Path,
    config: Dict[str, Any],
    progress_callback=None,
) -> List[Path]:
    """
    Convenience function to separate a file.
    
    Args:
        input_path: Path to input audio file
        output_dir: Directory to save output files
        config: Configuration dictionary
        progress_callback: Optional async callback for progress
        
    Returns:
        List of output file paths
    """
    engine = SeparationEngine(config)
    return await engine.separate(input_path, output_dir, progress_callback)


if __name__ == "__main__":
    # Test the engine
    import json
    
    config = {
        "model_name": "htdemucs_ft",
        "segment": 8.0,
        "overlap": 1.0,
        "shifts": 0,
        "output_format": "wav",
        "device": "cpu",
    }
    
    print("Separation Engine Test")
    print(f"PyTorch available: {TORCH_AVAILABLE}")
    print(f"Demucs available: {DEMUCS_AVAILABLE}")
    print(f"Librosa available: {LIBROSA_AVAILABLE}")
    print(f"Config: {json.dumps(config, indent=2)}")
