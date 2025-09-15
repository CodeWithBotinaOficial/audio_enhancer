from pydub import AudioSegment
from .base import NormalizationStrategy

class PeakNormalizer(NormalizationStrategy):
    """Normalizes audio to a specific peak level.

    This is a simple and fast normalization method, but it doesn't account for
    perceived loudness.
    """
    def __init__(self, target_dbfs: float = -1.0):
        self.target_dbfs = target_dbfs

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies peak normalization to the audio segment."""
        change_in_dbfs = self.target_dbfs - audio.max_dBFS
        return audio.apply_gain(change_in_dbfs)
