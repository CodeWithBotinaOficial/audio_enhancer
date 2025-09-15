import pytest
from pydub import AudioSegment
import numpy as np
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.noise_reduction.impulse_noise import ImpulseNoiseReducer
from audio_enhancer.noise_reduction.noise_synthesis import generate_noise

@pytest.fixture
def noisy_audio():
    """A sine wave with white noise."""
    from pydub.generators import Sine
    sine_wave = Sine(440).to_audio_segment(duration=1000, volume=-10)
    noise = generate_noise('white', 1000).apply_gain(-20)
    return sine_wave.overlay(noise)

def test_spectral_gating(noisy_audio):
    reducer = SpectralGatingNoiseReducer()
    processed_audio = reducer.process(noisy_audio)
    # A simple check: processed audio should have lower RMS energy than original
    assert processed_audio.rms < noisy_audio.rms

def test_impulse_noise_reducer():
    # Create a signal with a single impulse spike
    samples = np.zeros(1000, dtype=np.int16)
    samples[500] = 32767 # Max amplitude spike
    audio = AudioSegment(samples.tobytes(), frame_rate=44100, sample_width=2, channels=1)

    reducer = ImpulseNoiseReducer(kernel_size=3)
    processed_audio = reducer.process(audio)

    processed_samples = np.array(processed_audio.get_array_of_samples())
    # The spike should be gone (or significantly reduced)
    assert processed_samples[500] == 0
