from pydub import AudioSegment
import numpy as np
from .base import NormalizationStrategy

class RmsNormalizer(NormalizationStrategy):
    """Normalizes audio to a specific Root Mean Square (RMS) level.

    RMS normalization calculates the average energy of the signal to normalize
    the audio level, which is a better approximation of perceived loudness than
    peak normalization but simpler than LUFS.
    """
    def __init__(self, target_rms: float = -20.0):
        """Initializes the RmsNormalizer with a target RMS dB level.

        Args:
            target_rms (float): The desired average RMS level in decibels relative
                to full scale (dBFS). Defaults to -20.0.
        """
        self.target_rms = target_rms

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies RMS normalization to the input audio segment.

        Args:
            audio (AudioSegment): The input audio segment to normalize.

        Returns:
            AudioSegment: The RMS-normalized audio segment.
        """
        # Calculate the RMS of the original audio
        samples = np.array(audio.get_array_of_samples())
        # Avoid division by zero for silence
        if samples.any():
            current_rms_db = 20 * np.log10(np.sqrt(np.mean(np.square(samples / (2**15))))) 
            gain_db = self.target_rms - current_rms_db
            return audio.apply_gain(gain_db)
        return audio
