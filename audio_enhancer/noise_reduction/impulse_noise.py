from pydub import AudioSegment
import numpy as np
from scipy.signal import medfilt
from .base import NoiseReductionStrategy

class ImpulseNoiseReducer(NoiseReductionStrategy):
    """Reduces impulse noise (such as clicks, pops, or crackle) using a median filter.

    This strategy applies a one-dimensional median filter to the audio sample array
    to suppress sudden, high-amplitude spikes without heavily affecting the underlying audio.
    """
    def __init__(self, kernel_size: int = 3):
        """Initializes the ImpulseNoiseReducer with a specified kernel size.

        Args:
            kernel_size (int): The aperture size of the median filter.
                Must be a positive odd integer. If an even value is supplied,
                it will be incremented by 1 to make it odd. Defaults to 3.
        """
        # Kernel size must be odd
        self.kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies a median filter to the audio segment to remove impulse noise.

        Args:
            audio (AudioSegment): The input audio segment containing clicks or pops.

        Returns:
            AudioSegment: The clean, filtered audio segment.
        """
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)

        # Apply median filter
        filtered_samples = medfilt(samples, self.kernel_size)

        return AudioSegment(
            filtered_samples.astype(np.int16).tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )
