import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audio_enhancer.enhancer import AudioEnhancer
from audio_enhancer.normalization.lufs import LufsNormalizer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.noise_reduction.noise_synthesis import generate_noise

def main():
    """Demonstrates the audio enhancement pipeline."""
    # Create directories if they don't exist
    os.makedirs("examples/sample_audio", exist_ok=True)
    os.makedirs("examples/output", exist_ok=True)

    # --- Create a sample audio file for the demo ---
    # This simulates a real-world scenario where you have an input file.
    sample_rate = 44100
    # Create a 3-second sine wave at 440 Hz
    from pydub.generators import Sine
    sine_wave = Sine(440).to_audio_segment(duration=3000, volume=-10)
    # Create some background noise
    noise = generate_noise('white', 3000, sample_rate).apply_gain(-20)
    # Mix them together
    input_audio = sine_wave.overlay(noise)
    input_file = "examples/sample_audio/input.m4a"
    input_audio.export(input_file, format="wav")
    print(f"Generated sample audio file at: {input_file}")

    # --- Use the AudioEnhancer Facade ---
    enhancer = AudioEnhancer.get_instance()

    # 1. Load the audio file
    audio = enhancer.load_audio(input_file)

    # 2. Build a processing pipeline
    pipeline = (
        enhancer.get_builder()
        .add_step(SpectralGatingNoiseReducer())  # Remove background noise
        .add_step(LufsNormalizer(-16.0))         # Normalize to -16 LUFS
        .build()
    )

    # 3. Apply the pipeline
    enhanced_audio = pipeline.process(audio)

    # 4. Export to multiple formats
    output_mp3 = "examples/output/enhanced_demo.mp3"
    output_flac = "examples/output/enhanced_demo.flac"

    enhancer.export_audio(enhanced_audio, output_mp3, "mp3")
    enhancer.export_audio(enhanced_audio, output_flac, "flac")

    print(f"Enhancement complete. Output files:")
    print(f"- {output_mp3}")
    print(f"- {output_flac}")

if __name__ == "__main__":
    main()
