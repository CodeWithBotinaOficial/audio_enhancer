from pydub import AudioSegment
import numpy as np
import noisereduce as nr
from .base import NoiseReductionStrategy

class SpectralGatingNoiseReducer(NoiseReductionStrategy):
    """Reduces noise using spectral gating.

    This method is effective for continuous, stationary noise like hiss or hum.
    """
    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies spectral gating noise reduction."""
        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)

        # Perform noise reduction
        reduced_noise_samples = nr.reduce_noise(y=samples, sr=audio.frame_rate)

        # Convert back to AudioSegment
        return AudioSegment(
            reduced_noise_samples.astype(np.int16).tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )
