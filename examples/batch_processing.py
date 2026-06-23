"""Batch processing example for the AudioEnhancer library.

This script demonstrates how to search a directory for audio files and
process them in a batch loop, saving the enhanced versions to an output folder.
"""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audio_enhancer import AudioEnhancer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.normalization.rms import RmsNormalizer

def ensure_samples_exist():
    """Generates multiple mock audio files in a batch input directory."""
    os.makedirs("examples/batch_input", exist_ok=True)
    os.makedirs("examples/output", exist_ok=True)
    
    from pydub.generators import Sine
    from audio_enhancer.noise_reduction.noise_synthesis import generate_noise
    
    # Create sample 1
    file_1 = "examples/batch_input/sample_1.wav"
    if not os.path.exists(file_1):
        sine_1 = Sine(300).to_audio_segment(duration=2000, volume=-12)
        noise_1 = generate_noise('white', 2000, 44100).apply_gain(-25)
        sine_1.overlay(noise_1).export(file_1, format="wav")
        print(f"Generated {file_1}")
        
    # Create sample 2
    file_2 = "examples/batch_input/sample_2.wav"
    if not os.path.exists(file_2):
        sine_2 = Sine(600).to_audio_segment(duration=2500, volume=-8)
        noise_2 = generate_noise('white', 2500, 44100).apply_gain(-20)
        sine_2.overlay(noise_2).export(file_2, format="wav")
        print(f"Generated {file_2}")

def main():
    # Set up batch directory and mock files
    ensure_samples_exist()

    input_dir = "examples/batch_input"
    output_dir = "examples/output"

    # Get the facade instance
    enhancer = AudioEnhancer.get_instance()

    # Build a reusable processing pipeline
    pipeline = (
        enhancer.get_builder()
        .add_step(SpectralGatingNoiseReducer())
        .add_step(RmsNormalizer(target_rms=-18.0))
        .build()
    )

    # List all files in the batch directory
    files_to_process = [f for f in os.listdir(input_dir) if f.endswith('.wav')]
    print(f"Found {len(files_to_process)} audio files in {input_dir}")

    # Process files in a loop
    for filename in files_to_process:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"enhanced_{filename}")
        
        print(f"\nProcessing {filename}...")
        
        # 1. Load
        audio = enhancer.load_audio(input_path)
        
        # 2. Process
        enhanced_audio = pipeline.process(audio)
        
        # 3. Export
        print(f"Saving enhanced file to {output_path}")
        enhancer.export_audio(enhanced_audio, output_path, "wav")

    print("\nBatch processing complete!")

if __name__ == "__main__":
    main()
