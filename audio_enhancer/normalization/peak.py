from pydub import AudioSegment
from .base import NormalizationStrategy

class PeakNormalizer(NormalizationStrategy):
    """Normalizes audio to a specific peak level.

    Adjusts the gain of the audio segment so that the maximum peak reaches the
    specified level in decibels relative to full scale (dBFS).
    """
    def __init__(self, target_dbfs: float = -1.0):
        """Initializes the PeakNormalizer with a target peak dBFS.

        Args:
            target_dbfs (float): The target maximum peak level in dBFS.
                Defaults to -1.0.
        """
        self.target_dbfs = target_dbfs

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies peak normalization to the audio segment.

        Args:
            audio (AudioSegment): The input audio segment to normalize.

        Returns:
            AudioSegment: The peak-normalized audio segment.
        """
        change_in_dbfs = self.target_dbfs - audio.max_dBFS
        return audio.apply_gain(change_in_dbfs)
