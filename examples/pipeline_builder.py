"""Pipeline builder usage example for the AudioEnhancer library.

This script demonstrates how to construct a multi-stage audio enhancement
pipeline step-by-step using the fluent PipelineBuilder API.
"""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audio_enhancer import AudioEnhancer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.noise_reduction.impulse_noise import ImpulseNoiseReducer
from audio_enhancer.normalization.lufs import LufsNormalizer

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
    output_path = "examples/output/pipeline_output.wav"

    # 1. Get the facade instance
    enhancer = AudioEnhancer.get_instance()

    # 2. Load the audio
    audio = enhancer.load_audio(input_path)

    # 3. Build a pipeline using the builder
    print("Building audio enhancement pipeline...")
    pipeline = (
        enhancer.get_builder()
        .add_step(SpectralGatingNoiseReducer())   # Stage 1: Stationary noise gate
        .add_step(ImpulseNoiseReducer(kernel_size=5)) # Stage 2: Click/pop median filter
        .add_step(LufsNormalizer(target_lufs=-16.0)) # Stage 3: Broadcast LUFS normalizer
        .build()
    )

    # 4. Process the audio through the entire pipeline
    print("Processing audio through pipeline stages...")
    enhanced_audio = pipeline.process(audio)

    # 5. Export the output
    print(f"Exporting pipeline output: {output_path}")
    enhancer.export_audio(enhanced_audio, output_path, "wav")
    print("Done!")

if __name__ == "__main__":
    main()
