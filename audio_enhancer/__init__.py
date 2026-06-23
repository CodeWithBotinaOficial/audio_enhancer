"""AudioEnhancer package.

A production-grade Python audio enhancement toolkit that provides various
noise reduction strategies, loudness normalization models, and tools for
assembling custom processing pipelines.
"""

from audio_enhancer.enhancer import AudioEnhancer
from audio_enhancer.patterns.behavioral import AudioProcessingStep

__version__ = "0.1.0"

__all__ = ["AudioEnhancer", "AudioProcessingStep"]
