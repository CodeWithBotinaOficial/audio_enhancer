"""Shared utility functions for report generation."""

from functools import lru_cache
from pathlib import Path
from typing import Any
import librosa

@lru_cache(maxsize=16)
def _load_cached(path_str: str) -> tuple:
    """Load audio file via librosa and cache the result."""
    # librosa.load returns (y, sr)
    y, sr = librosa.load(path_str, sr=None, mono=True)
    return y, sr

def get_audio_data(path: Any) -> tuple:
    """Load audio as mono numpy array and sample rate.
    
    Uses an LRU cache internally to avoid repeated disk reads.
    """
    return _load_cached(str(path))

def setup_matplotlib_style():
    """Configure matplotlib for consistent, clean, and premium aesthetics."""
    import matplotlib.pyplot as plt
    plt.rcParams['figure.facecolor'] = '#fcfcfc'
    plt.rcParams['axes.facecolor'] = '#ffffff'
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.color'] = '#e2e8f0'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.linewidth'] = 0.5
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['text.color'] = '#1a202c'
    plt.rcParams['axes.labelcolor'] = '#1a202c'
    plt.rcParams['xtick.color'] = '#4a5568'
    plt.rcParams['ytick.color'] = '#4a5568'

def save_figure(fig, output_path: Any, dpi: int = 150):
    """Safely save a matplotlib figure and close it to free memory."""
    import matplotlib.pyplot as plt
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=dpi, bbox_inches='tight')
    plt.close(fig)

def add_metadata_text(fig, original_path: Any, processed_path: Any):
    """Add comparison metadata text at the bottom of the figure."""
    orig_name = Path(original_path).name
    proc_name = Path(processed_path).name
    fig.text(
        0.05, 0.01,
        f"Original File: {orig_name}   |   Processed File: {proc_name}",
        fontsize=8,
        color="#718096",
        ha="left",
        alpha=0.8
    )
