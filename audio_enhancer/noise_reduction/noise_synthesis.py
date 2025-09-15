import numpy as np
from pydub import AudioSegment

def generate_noise(noise_type: str, duration_ms: int, sample_rate: int = 44100) -> AudioSegment:
    """Generates white, pink, or brown noise.

    Args:
        noise_type: Type of noise ('white', 'pink', 'brown').
        duration_ms: Duration in milliseconds.
        sample_rate: The sample rate.

    Returns:
        An AudioSegment containing the generated noise.
    """
    num_samples = int(sample_rate * duration_ms / 1000.0)
    samples = np.random.randn(num_samples)

    if noise_type == 'pink':
        # Basic pink noise generation (Voss-McCartney algorithm)
        # This is a simplified version
        b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
        a = [1, -2.494956002, 2.017265875, -0.522189400]
        from scipy.signal import lfilter
        samples = lfilter(b, a, samples)
    elif noise_type == 'brown':
        # Basic brown noise (integration of white noise)
        samples = np.cumsum(samples)

    # Normalize to 16-bit range
    samples /= np.max(np.abs(samples))
    samples = (samples * (2**15 - 1)).astype(np.int16)

    return AudioSegment(
        samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=2, # 16-bit
        channels=1
    )
