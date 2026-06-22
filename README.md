# AudioEnhancer

A production-grade Python audio enhancement toolkit.

[![PyPI version](https://img.shields.io/pypi/v/audioenhancer)](https://img.shields.io/pypi/v/audioenhancer)
[![Python versions](https://img.shields.io/pypi/pyversions/audioenhancer)](https://img.shields.io/pypi/pyversions/audioenhancer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI Status](https://github.com/CodeWithBotinaOficial/audio_enhancer/actions/workflows/ci.yml/badge.svg)](https://github.com/CodeWithBotinaOficial/audio_enhancer/actions/workflows/ci.yml)

## Why AudioEnhancer?

AudioEnhancer is designed for developers who need robust, high-quality audio post-processing without complex configurations. By decoupling algorithms into standardized strategies, it offers a clean, extensible, and pattern-driven API for noise removal, level normalization, and seamless format conversions.

## Features

- 🤫 **Noise Removal**: Spectral gating for stationary noise and median filtering for impulse clicks/pops.
- 🎚️ **Loudness Normalization**: Support for Peak, RMS, and broadcast-standard LUFS (ITU-R BS.1770) normalization.
- 🔁 **Format Conversion**: Convert easily between standard formats like WAV, MP3, FLAC, and more.
- 🛠️ **Fluent Pipeline Builder**: Build and execute custom chains using a modern builder API.
- 🖥️ **Command-Line Interface (CLI)**: Powerful, Click-powered command-line interface for quick batch or single file processing.

## Prerequisites

This project requires [FFmpeg](https://ffmpeg.org/download.html) to be installed and available in your system's PATH.

- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt-get update && sudo apt-get install -y ffmpeg`
- **Windows**: Install via Chocolatey `choco install ffmpeg` or download binaries directly.

## Installation

### Standard Installation (from PyPI)

```bash
pip install audioenhancer
```

### Installation from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/CodeWithBotinaOficial/audio_enhancer.git
   cd audio_enhancer
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Interface (CLI)

The CLI provides a quick way to process audio files. You can run it as a module or after installing the package:

```bash
python -m audio_enhancer process-file examples/sample_audio/input.wav examples/output/output.mp3 --noise-profile spectral_gate --normalize lufs --lufs -16.0
```

### Library Usage

The project can be used as a Python library by importing the `AudioEnhancer` facade:

```python
from audio_enhancer import AudioEnhancer
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

- **Facade**: `AudioEnhancer` class provides a simple, high-level interface.
- **Strategy**: Different normalization and noise reduction algorithms are implemented as strategies.
- **Builder**: `PipelineBuilder` constructs complex processing pipelines step-by-step.
- **Singleton**: The `Logger` and `AudioEnhancer` use the Singleton pattern.
- **Factory Method**: Used to create different audio processors.

## Documentation

Full documentation, including tutorials, guide, and API reference, is available at [https://codewithbotinaoficial.github.io/audio_enhancer/](https://codewithbotinaoficial.github.io/audio_enhancer/).

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

Copyright (c) 2026 Diego Alejandro Botina (CodeWithBotina).
