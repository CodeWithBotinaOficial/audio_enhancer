from pydub import AudioSegment
import numpy as np
import noisereduce as nr
from .base import NoiseReductionStrategy

class SpectralGatingNoiseReducer(NoiseReductionStrategy):
    """Reduces noise using a spectral gating algorithm.

    This method is effective for continuous, stationary noise such as hiss, hum,
    fan noise, or background static. It utilizes the `noisereduce` library
    to estimate a noise gate threshold across frequency bins.
    """
    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies spectral gating noise reduction to the input audio segment.

        Args:
            audio (AudioSegment): The noisy input audio segment.

        Returns:
            AudioSegment: The processed audio segment with reduced stationary noise.
        """
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
