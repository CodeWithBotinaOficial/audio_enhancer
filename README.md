# AudioEnhancer

A production-grade Python audio enhancement toolkit.

## Features

- **Noise Removal**: Spectral gating, impulse noise removal, and more.
- **Audio Normalization**: Peak, RMS, and LUFS (EBU R128).
- **Format Conversion**: Convert between various audio formats like WAV, MP3, FLAC, etc.
- **Advanced Architecture**: Built with OOP and common software design patterns.

## Prerequisites

This project requires [FFmpeg](https://ffmpeg.org/download.html) to be installed and available in your system's PATH.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/CodeWithBotinaOficial/audio_enhancer.git
    cd audio_enhancer
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Usage

### Command-Line Interface (CLI)

The CLI provides a quick way to process audio files.

```bash
python cli.py process-file examples/sample_audio/input.wav examples/output/output.mp3 --noise-profile spectral_gate --normalize lufs --lufs -16.0
```

### Library Usage

The project can be used as a Python library by importing the `AudioEnhancer` facade.

```python
from audio_enhancer.enhancer import AudioEnhancer
from audio_enhancer.normalization.lufs import LufsNormalizer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer

def main():
    # Create an enhancer instance
    enhancer = AudioEnhancer.get_instance()

    # Load an audio file
    audio = enhancer.load_audio("examples/sample_audio/input.wav")

    # Create a processing pipeline
    pipeline = (
        enhancer.get_builder()
        .add_step(SpectralGatingNoiseReducer())
        .add_step(LufsNormalizer(-16.0))
        .build()
    )

    # Apply the pipeline
    enhanced_audio = pipeline.process(audio)

    # Export the result
    enhancer.export_audio(enhanced_audio, "examples/output/enhanced_audio.flac", "flac")
    print("Audio enhancement complete.")

if __name__ == "__main__":
    main()
```

## Design Patterns

This project serves as a practical example of various software design patterns:

-   **Facade**: `AudioEnhancer` class provides a simple, high-level interface.
-   **Strategy**: Different normalization and noise reduction algorithms are implemented as strategies.
-   **Builder**: `PipelineBuilder` constructs complex processing pipelines step-by-step.
-   **Singleton**: The `Logger` and `AudioEnhancer` use the Singleton pattern.
-   **Factory Method**: Used to create different audio processors.
-   ... and many more. See the `audio_enhancer/patterns/` directory for detailed examples.
