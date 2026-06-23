from pydub import AudioSegment
import numpy as np
import pyloudnorm as pyln
from .base import NormalizationStrategy

class LufsNormalizer(NormalizationStrategy):
    """Normalizes audio to a specific LUFS level using the ITU-R BS.1770 algorithm.

    Loudness Units Full Scale (LUFS) measures perceived loudness, making this
    method the standard for broadcast, podcasting, and streaming platforms.
    This class adapts the `pyloudnorm` library.
    """
    def __init__(self, target_lufs: float = -16.0):
        """Initializes the LUFS normalizer with a target level.

        Args:
            target_lufs (float): The desired integrated loudness level in LUFS.
                Defaults to -16.0 (the standard for podcasts/web audio).
        """
        self.target_lufs = target_lufs

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies LUFS normalization to the input audio segment.

        Adapts the `pyloudnorm` measurement library to perform loudness-based
        gain adjustments.

        Args:
            audio (AudioSegment): The input audio segment to normalize.

        Returns:
            AudioSegment: The normalized audio segment.
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
