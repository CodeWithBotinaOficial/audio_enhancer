# Visual Comparison Reports

AudioEnhancer provides a production-grade reporting system that generates visual analysis plots comparing original and processed audio files. This is extremely useful for verifying the effects of noise reduction and loudness normalization.

The reporting system supports generation of:
- **Spectrogram Comparisons**: Highlighting frequency distribution over time.
- **Waveform Comparisons**: Zoomed and full-scale overlays of signal amplitude.
- **Frequency Spectrum Comparisons**: Power Spectral Density (PSD) in decibels vs frequency.
- **HTML Summary Report**: A single compiled HTML file aggregating all visual plots.

---

## 1. Using from the CLI

To generate comparison reports via the CLI, pass the `--generate-report` flag to the `process-file` command. You can optionally control resolution with `--report-dpi`.

```bash
audioenhancer process-file input.wav output.wav \
  --noise-profile spectral_gate \
  --normalize lufs --lufs -14 \
  --generate-report \
  --report-dpi 150
```

On success, the reports are generated in the `.reports/` directory of your current working directory:
```
.reports/
├── input_spectrogram.png
├── input_waveform.png
├── input_frequency_spectrum.png
└── input_report_summary.html
```

---

## 2. Using from the Library Facade

The primary `AudioEnhancer` facade exposes a simple method to generate reports.

```python
from audio_enhancer import AudioEnhancer

enhancer = AudioEnhancer.get_instance()

# Generate reports after processing
report_paths = enhancer.generate_report(
    original_path="path/to/input.wav",
    processed_path="path/to/output.wav",
    output_dir=".reports"
)

for path in report_paths:
    print(f"Generated: {path}")
```

---

## 3. Custom Report Pipelines (Builder Pattern)

For advanced scenarios, you can use the `ReportBuilder` to customize which reports are compiled and configure plot settings.

```python
from audio_enhancer.reports import ReportBuilder

# Build a generator that only compiles Spectrogram and Waveform comparison reports
generator = (
    ReportBuilder(output_dir="custom_reports/")
    .add_spectrogram()
    .add_waveform()
    .set_dpi(200)
    .build()
)

# Run the generation pipeline
generator.generate_all("original.wav", "processed.wav")
```

---

## 4. Visualizing the Reports

To see the reporting system in action, check out the complete runnable script in [visual_reports.py](file:///home/Botina/development-environment/audio_enhancer/examples/visual_reports.py).

### Summary Report
The summary page compiles all plots into a unified HTML dashboard:

```html
<!-- Open .reports/{stem}_report_summary.html in your browser -->
```
Each plot highlights distinct audio characteristics:
- **Spectrogram**: Identifies stationary/impulse noise reduction across specific bands.
- **Waveform**: Compares peaks and reveals transient clipping or preservation.
- **Frequency Spectrum**: Plots smoothed PSD curves to compare the frequency response profile before and after processing.
