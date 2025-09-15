from pydub import AudioSegment
import numpy as np
from scipy.signal import medfilt
from .base import NoiseReductionStrategy

class ImpulseNoiseReducer(NoiseReductionStrategy):
    """Reduces impulse noise (clicks, pops) using a median filter.

    This is a simple but effective method for short, non-continuous noise.
    """
    def __init__(self, kernel_size=3):
        # Kernel size must be odd
        self.kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies a median filter to reduce impulse noise."""
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)

        # Apply median filter
        filtered_samples = medfilt(samples, self.kernel_size)

        return AudioSegment(
            filtered_samples.astype(np.int16).tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )
