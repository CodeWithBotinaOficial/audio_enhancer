"""Custom processor example for the AudioEnhancer library.

This script demonstrates how a library user can define their own custom audio
processing step (e.g., adding a simple fade-out effect) by subclassing the
base `AudioProcessingStep` class, and then integrate it seamlessly into a
PipelineBuilder chain.
"""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audio_enhancer import AudioEnhancer, AudioProcessingStep
from pydub import AudioSegment

class CustomFadeOutProcessor(AudioProcessingStep):
    """A custom processing step that applies a fade-out effect to the end of the audio.
    
    This implements the `AudioProcessingStep` abstract interface.
    """
    def __init__(self, duration_ms: int = 1000):
        """Initializes the custom processor with a fade duration.

        Args:
            duration_ms (int): The duration of the fade-out effect in milliseconds.
                Defaults to 1000 (1 second).
        """
        self.duration_ms = duration_ms

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Applies a fade-out to the AudioSegment.

        Args:
            audio (AudioSegment): The input audio segment.

        Returns:
            AudioSegment: The audio segment with fade-out applied.
        """
        print(f"Applying custom fade-out of {self.duration_ms} ms...")
        return audio.fade_out(self.duration_ms)

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
    # Ensure sample audio exists
    ensure_sample_exists()

    input_path = "examples/sample_audio/input.m4a"
    output_path = "examples/output/custom_processor_output.wav"

    # Get the facade instance
    enhancer = AudioEnhancer.get_instance()

    # Load audio
    audio = enhancer.load_audio(input_path)

    # Instantiate custom processor
    custom_step = CustomFadeOutProcessor(duration_ms=1500)

    # Chain it in a pipeline using the builder
    pipeline = (
        enhancer.get_builder()
        .add_step(custom_step)
        .build()
    )

    # Run the pipeline
    processed_audio = pipeline.process(audio)

    # Save output
    enhancer.export_audio(processed_audio, output_path, "wav")
    print(f"Successfully saved to {output_path}")

if __name__ == "__main__":
    main()
