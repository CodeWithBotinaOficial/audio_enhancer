# Installation

This section covers the system prerequisites and instructions to install AudioEnhancer.

## Prerequisites

Before installing the library, ensure that you have the following requirements:

1. **Python**: `Python >= 3.9`
2. **FFmpeg**: This package relies on `pydub`, which requires FFmpeg to decode and encode non-WAV formats.

### Installing FFmpeg

Depending on your operating system, install FFmpeg using one of the following methods:

=== "macOS"

    ```bash
    brew install ffmpeg
    ```

=== "Ubuntu / Debian"

    ```bash
    sudo apt-get update
    sudo apt-get install -y ffmpeg
    ```

=== "Windows"

    Using Chocolatey:
    ```bash
    choco install ffmpeg
    ```
    Or download the executable binaries directly from [ffmpeg.org](https://ffmpeg.org/download.html) and add them to your system's `PATH`.

---

## Installing the Package

### 1. Stable Release (via PyPI)

To install the latest stable version of `audioenhancer` from PyPI, run:

```bash
pip install audioenhancer
```

### 2. From Source (Development Mode)

If you wish to contribute to the package or use the latest developmental version, clone the repository and install it in editable mode:

```bash
git clone https://github.com/CodeWithBotinaOficial/audio_enhancer.git
cd audio_enhancer
pip install -e .
```

---

## Verifying the Installation

To verify that the library and CLI have been successfully installed, execute:

```bash
python -m audio_enhancer --help
```

You should see a Click CLI help menu listing the available options and commands.
