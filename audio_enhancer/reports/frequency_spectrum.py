"""Frequency spectrum comparison report implementation."""

from pathlib import Path
from typing import Any
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

from .base import BaseReport
from .config import DEFAULT_DPI, DEFAULT_FIGSIZE, COLOR_ORIGINAL, COLOR_PROCESSED, COLOR_DIFF
from .utils import setup_matplotlib_style, save_figure, add_metadata_text, get_audio_data

class FrequencySpectrumReport(BaseReport):
    """Generates FFT/PSD frequency spectrum comparison reports."""
    
    def __init__(self, output_dir: Any, dpi: int = DEFAULT_DPI, figsize: tuple = DEFAULT_FIGSIZE):
        super().__init__(output_dir, dpi, figsize)
        
    @property
    def report_name(self) -> str:
        return "Frequency Spectrum Comparison"
        
    def generate(self, original_audio: Any, processed_audio: Any, 
                 original_path: Path, processed_path: Path) -> Path:
        setup_matplotlib_style()
        
        # Retrieve sample rates
        _, sr_orig = get_audio_data(original_path)
        _, sr_proc = get_audio_data(processed_path)
        
        # We construct a figure with 2 side-by-side subplots (PSD overlay & Difference)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize, dpi=self.dpi)
        
        # Compute Power Spectral Density (PSD) using Welch's method for smooth curves
        nperseg = min(len(original_audio), len(processed_audio), 4096)
        # Handle cases where audio signal is shorter than default segment size
        if nperseg < 256:
            nperseg = max(16, nperseg)
            
        freqs_orig, psd_orig = scipy.signal.welch(original_audio, fs=sr_orig, nperseg=nperseg)
        freqs_proc, psd_proc = scipy.signal.welch(processed_audio, fs=sr_proc, nperseg=nperseg)
        
        # Convert PSD to dB
        psd_orig_db = 10 * np.log10(np.maximum(psd_orig, 1e-12))
        psd_proc_db = 10 * np.log10(np.maximum(psd_proc, 1e-12))
        
        # Overlay PSD Plot (logarithmic scale)
        ax1.semilogx(freqs_orig, psd_orig_db, color=COLOR_ORIGINAL, alpha=0.7, label="Original")
        ax1.semilogx(freqs_proc, psd_proc_db, color=COLOR_PROCESSED, alpha=0.7, label="Processed")
        ax1.set_title("Power Spectral Density Comparison")
        ax1.set_xlabel("Frequency (Hz)")
        ax1.set_ylabel("Power Spectral Density (dB/Hz)")
        ax1.set_xlim(20, min(sr_orig, sr_proc) / 2)
        ax1.legend(loc="upper right")
        
        # Interpolate processed PSD to original frequency bins to compute exact differences
        psd_proc_db_interp = np.interp(freqs_orig, freqs_proc, psd_proc_db)
        diff_db = psd_proc_db_interp - psd_orig_db
        
        # Difference Plot
        ax2.semilogx(freqs_orig, diff_db, color=COLOR_DIFF, alpha=0.8, label="Difference (Proc - Orig)")
        ax2.axhline(0, color="gray", linestyle="--", alpha=0.5)
        ax2.set_title("Frequency Magnitude Difference")
        ax2.set_xlabel("Frequency (Hz)")
        ax2.set_ylabel("Magnitude Difference (dB)")
        ax2.set_xlim(20, min(sr_orig, sr_proc) / 2)
        ax2.legend(loc="upper right")
        
        # Adjust layout
        fig.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        add_metadata_text(fig, original_path, processed_path)
        
        stem = original_path.stem
        output_file = self.output_dir / f"{stem}_frequency_spectrum.png"
        save_figure(fig, output_file, self.dpi)
        
        return output_file
