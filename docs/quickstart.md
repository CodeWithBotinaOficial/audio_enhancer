# Quick Start

Get started with AudioEnhancer in just a few minutes using the library API or command-line interface.

## Library Quick Start

Enhance audio in 3 simple steps: load the file, chain your processing steps in a pipeline, and export the result.

### 1. The Code

Create a Python script and add the following code:

```python
from audio_enhancer import AudioEnhancer
from audio_enhancer.normalization.lufs import LufsNormalizer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer

def main():
    # 1. Get the Singleton enhancer instance
    enhancer = AudioEnhancer.get_instance()

    # 2. Load the input file
    audio = enhancer.load_audio("input.wav")

    # 3. Create a processing pipeline and execute
    pipeline = (
        enhancer.get_builder()
        .add_step(SpectralGatingNoiseReducer())  # Reduce static hiss
        .add_step(LufsNormalizer(-16.0))         # Normalize perceived loudness to -16 LUFS
        .build()
    )
    enhanced_audio = pipeline.process(audio)

    # 4. Export the resulting audio segment
    enhancer.export_audio(enhanced_audio, "output.flac", "flac")
    print("Audio processing completed successfully.")

if __name__ == "__main__":
    main()
```

### 2. Expected Output

When running the script, you should see logs indicating loading and exporting progress:

```text
2026-06-22 18:50:00 - AudioEnhancer - INFO - Loading audio from: input.wav
2026-06-22 18:50:02 - AudioEnhancer - INFO - Exporting audio to: output.flac in format: flac
Audio processing completed successfully.
```

---

## CLI Quick Start

You can also run audio enhancement processes directly from the terminal without writing any code.

Run the following command:

```bash
python -m audio_enhancer process-file input.wav output.mp3 \
  --noise-profile spectral_gate \
  --normalize lufs \
  --lufs -16.0
```

### Options Explained

- `process-file`: The subcommand to run single-file processing.
- `input.wav`: The path to the source audio file.
- `output.mp3`: The path to the destination file.
- `--noise-profile spectral_gate`: Applies spectral gating noise reduction.
- `--normalize lufs`: Enables loudness normalization.
- `--lufs -16.0`: Targets -16.0 LUFS loudness.
