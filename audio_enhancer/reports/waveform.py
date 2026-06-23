"""Waveform comparison report implementation."""

from pathlib import Path
from typing import Any
import numpy as np
import matplotlib.pyplot as plt

from .base import BaseReport
from .config import DEFAULT_DPI, DEFAULT_FIGSIZE, COLOR_ORIGINAL, COLOR_PROCESSED
from .utils import setup_matplotlib_style, save_figure, add_metadata_text, get_audio_data

class WaveformReport(BaseReport):
    """Generates waveform amplitude comparison reports."""
    
    def __init__(self, output_dir: Any, dpi: int = DEFAULT_DPI, figsize: tuple = DEFAULT_FIGSIZE):
        super().__init__(output_dir, dpi, figsize)
        
    @property
    def report_name(self) -> str:
        return "Waveform Comparison"
        
    def generate(self, original_audio: Any, processed_audio: Any, 
                 original_path: Path, processed_path: Path) -> Path:
        setup_matplotlib_style()
        
        # Retrieve sample rates
        _, sr_orig = get_audio_data(original_path)
        _, sr_proc = get_audio_data(processed_path)
        
        # We construct a figure with 2 subplots (Full Waveform and Zoomed View)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], self.figsize[1] + 2), dpi=self.dpi)
        
        # Full Waveform Calculations
        t_orig = np.arange(len(original_audio)) / sr_orig
        t_proc = np.arange(len(processed_audio)) / sr_proc
        
        # Plot full original and processed overlaid
        ax1.plot(t_orig, original_audio, color=COLOR_ORIGINAL, alpha=0.5, label="Original")
        ax1.plot(t_proc, processed_audio, color=COLOR_PROCESSED, alpha=0.6, label="Processed")
        ax1.set_title("Full Audio Waveform Comparison")
        ax1.set_xlabel("Time (seconds)")
        ax1.set_ylabel("Amplitude")
        ax1.legend(loc="upper right")
        
        # Zoomed-In Section
        zoom_sec = 0.1  # 100ms
        mid_orig_sec = t_orig[-1] / 2
        mid_proc_sec = t_proc[-1] / 2
        
        # Original zoomed segment
        zoom_orig_start = int(max(0, (mid_orig_sec - zoom_sec / 2) * sr_orig))
        zoom_orig_end = int(min(len(original_audio), (mid_orig_sec + zoom_sec / 2) * sr_orig))
        t_orig_zoom = t_orig[zoom_orig_start:zoom_orig_end]
        audio_orig_zoom = original_audio[zoom_orig_start:zoom_orig_end]
        
        # Processed zoomed segment
        zoom_proc_start = int(max(0, (mid_proc_sec - zoom_sec / 2) * sr_proc))
        zoom_proc_end = int(min(len(processed_audio), (mid_proc_sec + zoom_sec / 2) * sr_proc))
        t_proc_zoom = t_proc[zoom_proc_start:zoom_proc_end]
        audio_proc_zoom = processed_audio[zoom_proc_start:zoom_proc_end]
        
        # Plot zoomed-in comparison
        ax2.plot(t_orig_zoom, audio_orig_zoom, color=COLOR_ORIGINAL, alpha=0.7, label="Original")
        ax2.plot(t_proc_zoom, audio_proc_zoom, color=COLOR_PROCESSED, alpha=0.8, label="Processed")
        ax2.set_title("Zoomed Waveform Comparison (100ms Window)")
        ax2.set_xlabel("Time (seconds)")
        ax2.set_ylabel("Amplitude")
        ax2.legend(loc="upper right")
        
        # Adjust layout
        fig.tight_layout()
        plt.subplots_adjust(bottom=0.12)
        add_metadata_text(fig, original_path, processed_path)
        
        stem = original_path.stem
        output_file = self.output_dir / f"{stem}_waveform.png"
        save_figure(fig, output_file, self.dpi)
        
        return output_file
