"""Basic usage example for the AudioEnhancer library.

This script demonstrates how to load an audio file, apply noise reduction
and peak normalization, and export the result using the AudioEnhancer facade.
"""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audio_enhancer import AudioEnhancer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.normalization.peak import PeakNormalizer

def ensure_sample_exists():
    """Generates a mock audio file if it doesn't exist."""
    os.makedirs("examples/sample_audio", exist_ok=True)
    os.makedirs("examples/output", exist_ok=True)
    
    input_file = "examples/sample_audio/input.m4a"
    if not os.path.exists(input_file):
        print("Generating mock sample audio file...")
        from pydub.generators import Sine
        from audio_enhancer.noise_reduction.noise_synthesis import generate_noise
        
        sine_wave = Sine(440).to_audio_segment(duration=3000, volume=-10)
        noise = generate_noise('white', 3000, 44100).apply_gain(-20)
        input_audio = sine_wave.overlay(noise)
        input_audio.export(input_file, format="wav")
        print(f"Mock sample generated at {input_file}")

def main():
    # Ensure sample audio files exist
    ensure_sample_exists()

    input_path = "examples/sample_audio/input.m4a"
    output_path = "examples/output/basic_output.wav"

    # 1. Get the facade instance
    enhancer = AudioEnhancer.get_instance()

    # 2. Load the noisy audio
    print(f"Loading: {input_path}")
    audio = enhancer.load_audio(input_path)

    # 3. Create individual processors
    noise_reducer = SpectralGatingNoiseReducer()
    normalizer = PeakNormalizer(target_dbfs=-3.0)

    # 4. Process audio sequentially
    print("Reducing noise...")
    reduced_audio = noise_reducer.process(audio)
    
    print("Normalizing peak levels...")
    normalized_audio = normalizer.process(reduced_audio)

    # 5. Export the result
    print(f"Exporting: {output_path}")
    enhancer.export_audio(normalized_audio, output_path, "wav")
    print("Done!")

if __name__ == "__main__":
    main()
