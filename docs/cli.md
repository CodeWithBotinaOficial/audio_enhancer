# Command-Line Interface (CLI)

AudioEnhancer ships with a powerful command-line interface based on Click, letting you execute common operations directly from your terminal.

## Run Commands

Run the CLI using the package runner:

```bash
python -m audio_enhancer [OPTIONS] COMMAND [ARGS]...
```

---

## Global Options

- `--help`: Shows the help message and exits.

---

## Commands

### `process-file`

Processes a single audio file, applying the specified noise reduction strategies and normalization profiles.

#### Syntax

```bash
python -m audio_enhancer process-file [OPTIONS] INPUT_FILE OUTPUT_FILE
```

#### Arguments

- `INPUT_FILE`: Path to the source file to process (must exist on disk).
- `OUTPUT_FILE`: Path to save the processed output file. The output format is automatically derived from the file extension (e.g. `.wav`, `.mp3`, `.flac`).

#### Options

- `--noise-profile [spectral_gate|impulse|none]`  
  The noise reduction method to apply. Defaults to `none`.
    - `spectral_gate`: High-quality spectral gating for stationary noises (hiss, static).
    - `impulse`: Median filter designed to reduce transient pops, crackles, and clicks.
- `--normalize [peak|rms|lufs|none]`  
  The normalization method to apply. Defaults to `none`.
    - `peak`: Level normalization relative to full-scale peak.
    - `rms`: Normalization based on average root-mean-square amplitude.
    - `lufs`: Perceived loudness normalization matching broadcast standard ITU-R BS.1770.
- `--lufs FLOAT`  
  Target integrated loudness level in LUFS. Only active when `--normalize lufs` is set. Defaults to `-16.0`.
- `--peak-db FLOAT`  
  Target peak decibels relative to full scale (dBFS). Only active when `--normalize peak` is set. Defaults to `-1.0`.
- `--rms-db FLOAT`  
  Target average RMS level in dBFS. Only active when `--normalize rms` is set. Defaults to `-20.0`.

---

## Usage Examples

### 1. Podcast Processing (LUFS normalization)
Remove static background hum and normalize loudness to podcast standards (-16 LUFS):

```bash
python -m audio_enhancer process-file input.wav output.mp3 \
  --noise-profile spectral_gate \
  --normalize lufs \
  --lufs -16.0
```

### 2. Remove Clicks & Normalize Peak
Remove record pop noise and normalize peak level to -3.0 dBFS:

```bash
python -m audio_enhancer process-file raw_vinyl.wav clean_vinyl.wav \
  --noise-profile impulse \
  --normalize peak \
  --peak-db -3.0
```

### 3. Audio Format Conversion
Convert from a WAV recording to a compressed MP3 file without applying extra filters:

```bash
python -m audio_enhancer process-file input.wav output.mp3
```
