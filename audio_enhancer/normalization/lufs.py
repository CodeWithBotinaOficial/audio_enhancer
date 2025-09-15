from pydub import AudioSegment
import numpy as np
import pyloudnorm as pyln
from .base import NormalizationStrategy

class LufsNormalizer(NormalizationStrategy):
    """Normalizes audio to a specific LUFS level using the ITU-BS.1770 algorithm.

    This is the standard for broadcast and streaming, providing the most accurate
    measure of perceived loudness.
    """
    def __init__(self, target_lufs: float = -16.0):
        self.target_lufs = target_lufs

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies LUFS normalization.
        This method demonstrates the Adapter pattern by adapting the `pyloudnorm` library
        to our `NormalizationStrategy` interface.
        """
        # Convert audio to numpy array for pyloudnorm
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        samples = samples / (2**15) # Normalize to -1.0 to 1.0

        # Measure the loudness
        meter = pyln.Meter(audio.frame_rate)
        loudness = meter.integrated_loudness(samples)

        # Calculate the gain needed
        gain_db = self.target_lufs - loudness

        # Apply the gain
        return audio.apply_gain(gain_db)
