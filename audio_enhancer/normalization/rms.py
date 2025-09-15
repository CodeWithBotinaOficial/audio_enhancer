from pydub import AudioSegment
import numpy as np
from .base import NormalizationStrategy

class RmsNormalizer(NormalizationStrategy):
    """Normalizes audio to a specific RMS level.

    RMS normalization can provide a more consistent loudness level than peak
    normalization, but it's less sophisticated than LUFS.
    """
    def __init__(self, target_rms: float = -20.0):
        self.target_rms = target_rms

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies RMS normalization."""
        # Calculate the RMS of the original audio
        samples = np.array(audio.get_array_of_samples())
        # Avoid division by zero for silence
        if samples.any():
            current_rms_db = 20 * np.log10(np.sqrt(np.mean(np.square(samples / (2**15))))) 
            gain_db = self.target_rms - current_rms_db
            return audio.apply_gain(gain_db)
        return audio
