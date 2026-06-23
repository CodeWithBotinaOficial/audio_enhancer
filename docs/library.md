# Library Usage

This section details how to use AudioEnhancer as a Python package in your own codebase.

## Facade Pattern

The package exposes the `AudioEnhancer` class, which serves as a **Facade** to hide the internal complexity of loaders, exporters, and builder patterns. 

Additionally, `AudioEnhancer` implements the **Singleton** pattern, meaning you can retrieve the active instance from anywhere in your code using:

```python
from audio_enhancer import AudioEnhancer

enhancer = AudioEnhancer.get_instance()
```

---

## Loading and Exporting Audio

### 1. Load Audio

The facade's `load_audio` method internally uses `pydub.AudioSegment.from_file`. Because it uses FFmpeg under the hood, it supports decoding almost any audio format:

```python
audio = enhancer.load_audio("path/to/input.mp3")
```

The method returns a `pydub.AudioSegment` object representing the raw audio samples and metadata.

### 2. Export Audio

Save your processed `AudioSegment` back to disk in the format of your choice:

```python
enhancer.export_audio(audio, "path/to/output.flac", format="flac")
```

Supported formats include: `wav`, `mp3`, `ogg`, `flac`, `m4a`, etc.

---

## Processing Pipelines

To apply processing steps (such as noise reduction and level adjustment) to an audio file, you construct a processing `Pipeline`.

A `Pipeline` coordinates one or more `AudioProcessingStep` strategies, running them sequentially.

Here is a typical flow:

```python
from audio_enhancer import AudioEnhancer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.normalization.peak import PeakNormalizer

enhancer = AudioEnhancer.get_instance()
audio = enhancer.load_audio("recording.wav")

# 1. Access the builder
builder = enhancer.get_builder()

# 2. Configure steps
builder.add_step(SpectralGatingNoiseReducer())
builder.add_step(PeakNormalizer(target_dbfs=-2.0))

# 3. Build and execute pipeline
pipeline = builder.build()
processed_audio = pipeline.process(audio)

# 4. Save result
enhancer.export_audio(processed_audio, "processed_recording.wav", "wav")
```
