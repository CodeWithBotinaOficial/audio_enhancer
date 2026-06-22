# Examples

Explore these practical examples demonstrating how to use the AudioEnhancer package in different scenarios.

All code files are located in the `examples/` directory of the repository.

---

## 1. Basic Library Usage (`examples/basic_cli.py`)

This script demonstrates how to load an audio file, apply noise reduction and peak normalization, and export the result using the AudioEnhancer facade.

```python
import os
import sys

from audio_enhancer import AudioEnhancer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.normalization.peak import PeakNormalizer

def main():
    input_path = "examples/sample_audio/input.m4a"
    output_path = "examples/output/basic_output.wav"

    # 1. Get the facade instance
    enhancer = AudioEnhancer.get_instance()

    # 2. Load the noisy audio
    audio = enhancer.load_audio(input_path)

    # 3. Create individual processors
    noise_reducer = SpectralGatingNoiseReducer()
    normalizer = PeakNormalizer(target_dbfs=-3.0)

    # 4. Process audio sequentially
    reduced_audio = noise_reducer.process(audio)
    normalized_audio = normalizer.process(reduced_audio)

    # 5. Export the result
    enhancer.export_audio(normalized_audio, output_path, "wav")
    print("Processing complete!")

if __name__ == "__main__":
    main()
```

---

## 2. Pipeline Builder (`examples/pipeline_builder.py`)

This script demonstrates how to construct a multi-stage audio enhancement pipeline step-by-step using the fluent PipelineBuilder API.

```python
from audio_enhancer import AudioEnhancer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.noise_reduction.impulse_noise import ImpulseNoiseReducer
from audio_enhancer.normalization.lufs import LufsNormalizer

def main():
    input_path = "examples/sample_audio/input.m4a"
    output_path = "examples/output/pipeline_output.wav"

    # 1. Get the facade instance
    enhancer = AudioEnhancer.get_instance()

    # 2. Load the audio
    audio = enhancer.load_audio(input_path)

    # 3. Build a pipeline using the builder
    pipeline = (
        enhancer.get_builder()
        .add_step(SpectralGatingNoiseReducer())   # Stage 1: Stationary noise gate
        .add_step(ImpulseNoiseReducer(kernel_size=5)) # Stage 2: Click/pop median filter
        .add_step(LufsNormalizer(target_lufs=-16.0)) # Stage 3: Broadcast LUFS normalizer
        .build()
    )

    # 4. Process the audio through the entire pipeline
    enhanced_audio = pipeline.process(audio)

    # 5. Export the output
    enhancer.export_audio(enhanced_audio, output_path, "wav")
    print("Pipeline processing complete!")

if __name__ == "__main__":
    main()
```

---

## 3. Batch Processing (`examples/batch_processing.py`)

This script demonstrates how to search a directory for audio files and process them in a batch loop, saving the enhanced versions to an output folder.

```python
import os
from audio_enhancer import AudioEnhancer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.normalization.rms import RmsNormalizer

def main():
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

    # Process files in a loop
    for filename in files_to_process:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"enhanced_{filename}")
        
        # 1. Load
        audio = enhancer.load_audio(input_path)
        
        # 2. Process
        enhanced_audio = pipeline.process(audio)
        
        # 3. Export
        enhancer.export_audio(enhanced_audio, output_path, "wav")

    print("Batch processing complete!")

if __name__ == "__main__":
    main()
```

---

## 4. Custom Processor (`examples/custom_processor.py`)

This script demonstrates how a library user can define their own custom audio processing step (e.g., adding a simple fade-out effect) by subclassing the base `AudioProcessingStep` class, and then integrate it seamlessly into a PipelineBuilder chain.

```python
from audio_enhancer import AudioEnhancer, AudioProcessingStep
from pydub import AudioSegment

class CustomFadeOutProcessor(AudioProcessingStep):
    """A custom processing step that applies a fade-out effect to the end of the audio.
    
    This implements the `AudioProcessingStep` abstract interface.
    """
    def __init__(self, duration_ms: int = 1000):
        self.duration_ms = duration_ms

    def process(self, audio: AudioSegment) -> AudioSegment:
        print(f"Applying custom fade-out of {self.duration_ms} ms...")
        return audio.fade_out(self.duration_ms)

def main():
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
    print("Custom step processing complete!")

if __name__ == "__main__":
    main()
```
