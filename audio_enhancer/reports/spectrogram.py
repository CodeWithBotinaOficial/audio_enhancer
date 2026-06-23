"""Spectrogram comparison report implementation."""

from pathlib import Path
from typing import Any
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

from .base import BaseReport
from .config import DEFAULT_DPI, DEFAULT_FIGSIZE
from .utils import setup_matplotlib_style, save_figure, add_metadata_text, get_audio_data

class SpectrogramReport(BaseReport):
    """Generates comparison spectrograms for original and processed audio."""
    
    def __init__(self, output_dir: Any, dpi: int = DEFAULT_DPI, figsize: tuple = DEFAULT_FIGSIZE):
        super().__init__(output_dir, dpi, figsize)
        
    @property
    def report_name(self) -> str:
        return "Spectrogram Comparison"
        
    def generate(self, original_audio: Any, processed_audio: Any, 
                 original_path: Path, processed_path: Path) -> Path:
        setup_matplotlib_style()
        
        # Retrieve sample rates
        _, sr_orig = get_audio_data(original_path)
        _, sr_proc = get_audio_data(processed_path)
        
        # Subplots: Original, Processed, and Difference
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5), dpi=self.dpi)
        
        # Compute spectrograms using STFT
        orig_stft = np.abs(librosa.stft(original_audio))
        proc_stft = np.abs(librosa.stft(processed_audio))
        
        # Standardize sizes for difference matrix
        min_bins = min(orig_stft.shape[0], proc_stft.shape[0])
        min_frames = min(orig_stft.shape[1], proc_stft.shape[1])
        
        orig_trimmed = orig_stft[:min_bins, :min_frames]
        proc_trimmed = proc_stft[:min_bins, :min_frames]
        diff_stft = proc_trimmed - orig_trimmed
        
        # Plot Original Spectrogram
        orig_db = librosa.amplitude_to_db(orig_stft, ref=np.max)
        im1 = librosa.display.specshow(
            orig_db, sr=sr_orig, x_axis='time', y_axis='linear', ax=ax1, cmap='viridis'
        )
        fig.colorbar(im1, ax=ax1, format="%+2.0f dB")
        ax1.set_title("Original Spectrogram")
        
        # Plot Processed Spectrogram
        proc_db = librosa.amplitude_to_db(proc_stft, ref=np.max)
        im2 = librosa.display.specshow(
            proc_db, sr=sr_proc, x_axis='time', y_axis='linear', ax=ax2, cmap='viridis'
        )
        fig.colorbar(im2, ax=ax2, format="%+2.0f dB")
        ax2.set_title("Processed Spectrogram")
        
        # Plot Difference Spectrogram
        diff_db = librosa.amplitude_to_db(np.abs(diff_stft), ref=np.max)
        im3 = librosa.display.specshow(
            diff_db, sr=sr_orig, x_axis='time', y_axis='linear', ax=ax3, cmap='magma'
        )
        fig.colorbar(im3, ax=ax3, format="%+2.0f dB")
        ax3.set_title("Difference Magnitude")
        
        # Adjust layouts
        fig.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        add_metadata_text(fig, original_path, processed_path)
        
        stem = original_path.stem
        output_file = self.output_dir / f"{stem}_spectrogram.png"
        save_figure(fig, output_file, self.dpi)
        
        return output_file
