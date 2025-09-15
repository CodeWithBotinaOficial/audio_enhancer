import pytest
from pydub import AudioSegment
from audio_enhancer.normalization.peak import PeakNormalizer
from audio_enhancer.normalization.lufs import LufsNormalizer
import numpy as np

@pytest.fixture
def silent_audio():
    """A silent audio segment."""
    return AudioSegment.silent(duration=1000)

@pytest.fixture
def sine_wave_audio():
    """A sine wave audio segment."""
    sample_rate = 44100
    freq = 440
    duration = 1.0
    t = np.linspace(0., duration, int(sample_rate * duration))
    amplitude = np.iinfo(np.int16).max * 0.5
    data = amplitude * np.sin(2. * np.pi * freq * t)
    return AudioSegment(data.astype(np.int16).tobytes(), sample_width=2, frame_rate=sample_rate, channels=1)

def test_peak_normalizer(sine_wave_audio):
    normalizer = PeakNormalizer(target_dbfs=-3.0)
    normalized_audio = normalizer.process(sine_wave_audio)
    assert np.isclose(normalized_audio.max_dBFS, -3.0, atol=0.1)

def test_lufs_normalizer(sine_wave_audio):
    target_lufs = -23.0
    normalizer = LufsNormalizer(target_lufs=target_lufs)
    normalized_audio = normalizer.process(sine_wave_audio)
    
    # Re-measure to verify
    import pyloudnorm as pyln
    samples = np.array(normalized_audio.get_array_of_samples()).astype(np.float32)
    samples = samples / (2**15)
    meter = pyln.Meter(normalized_audio.frame_rate)
    loudness = meter.integrated_loudness(samples)
    assert np.isclose(loudness, target_lufs, atol=1.0) # LUFS can have some tolerance
