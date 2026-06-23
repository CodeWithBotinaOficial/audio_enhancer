"""
Example: Generating visual reports for audio processing.

This example demonstrates how to use the ReportGenerator
to create spectrograms, waveforms, and frequency spectrum
comparisons between original and processed audio.
"""
import os
import sys

# Add project root to Python path to ensure local import works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audio_enhancer import AudioEnhancer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.normalization.lufs import LufsNormalizer

def main():
    # Make sure output directories exist
    os.makedirs("examples/sample_audio", exist_ok=True)
    os.makedirs("examples/output", exist_ok=True)
    
    input_file = "examples/sample_audio/input.wav"
    output_file = "examples/output/enhanced.wav"
    
    # --- Create a sample audio file if it doesn't exist ---
    if not os.path.exists(input_file):
        print(f"Creating sample input audio at: {input_file}")
        from pydub.generators import Sine
        from audio_enhancer.noise_reduction.noise_synthesis import generate_noise
        # 3-second sine wave at 440 Hz
        sine_wave = Sine(440).to_audio_segment(duration=3000, volume=-10)
        # White noise mixed in
        noise = generate_noise('white', 3000, 44100).apply_gain(-18)
        input_audio = sine_wave.overlay(noise)
        input_audio.export(input_file, format="wav")
        
    enhancer = AudioEnhancer.get_instance()
    
    # Load and process audio
    print(f"Loading original audio from: {input_file}")
    audio = enhancer.load_audio(input_file)
    
    print("Applying enhancement pipeline...")
    pipeline = (
        enhancer.get_builder()
        .add_step(SpectralGatingNoiseReducer())
        .add_step(LufsNormalizer(-14.0))
        .build()
    )
    
    enhanced = pipeline.process(audio)
    print(f"Exporting processed audio to: {output_file}")
    enhancer.export_audio(enhanced, output_file, "wav")
    
    # Generate visual reports
    print("Generating visual comparison reports...")
    report_paths = enhancer.generate_report(
        input_file,
        output_file,
        output_dir="examples/.reports"
    )
    
    print("\nSuccessfully generated reports:")
    for path in report_paths:
        print(f"  - {path}")

if __name__ == "__main__":
    main()
