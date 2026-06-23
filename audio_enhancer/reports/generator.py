"""Report generator facade, factory, and builder implementations."""

from datetime import datetime
from pathlib import Path
from typing import Any, List
import numpy as np

from .base import BaseReport
from .utils import get_audio_data
from .spectrogram import SpectrogramReport
from .waveform import WaveformReport
from .frequency_spectrum import FrequencySpectrumReport

class ReportFactory:
    """Factory to instantiate report generators by name."""
    
    @staticmethod
    def create_report(report_name: str, output_dir: Any, **kwargs) -> BaseReport:
        """Create a report instance by name.
        
        Args:
            report_name: Name of the report ('spectrogram', 'waveform', 'frequency_spectrum')
            output_dir: Output directory for the report
            
        Returns:
            An instance of BaseReport subclass.
        """
        name_lower = report_name.lower().strip()
        if name_lower == "spectrogram":
            return SpectrogramReport(output_dir, **kwargs)
        elif name_lower == "waveform":
            return WaveformReport(output_dir, **kwargs)
        elif name_lower in ("frequency_spectrum", "frequency"):
            return FrequencySpectrumReport(output_dir, **kwargs)
        else:
            raise ValueError(f"Unknown report type: {report_name}")


class ReportGenerator:
    """Facade for generating comprehensive audio processing reports."""
    
    def __init__(self, output_dir: str = ".reports", dpi: int = 150):
        self.output_dir = Path(output_dir)
        self.dpi = dpi
        self._reports: List[BaseReport] = []
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def add_report(self, report: BaseReport) -> "ReportGenerator":
        """Add a report strategy to the generator list.
        
        Returns:
            self for method chaining.
        """
        self._reports.append(report)
        return self
    
    def generate_all(self, original_path: str, processed_path: str) -> List[Path]:
        """Generate all registered reports and return paths to generated files.
        
        Also generates a compiled HTML summary report comparing the files.
        """
        # Load audio data once (uses caching internally)
        original_audio, _ = get_audio_data(original_path)
        processed_audio, _ = get_audio_data(processed_path)
        
        generated = []
        for report in self._reports:
            path = report.generate(
                original_audio, processed_audio,
                Path(original_path), Path(processed_path)
            )
            generated.append(path)
            
        # Compile HTML summary report
        html_path = self._compile_html_summary(original_path, processed_path, generated)
        generated.append(html_path)
        
        return generated
    
    def _compile_html_summary(self, original_path: str, processed_path: str, generated_pngs: List[Path]) -> Path:
        """Compile comparison reports into a single responsive HTML page."""
        orig_name = Path(original_path).name
        proc_name = Path(processed_path).name
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stem = Path(original_path).stem
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Enhancer Comparison Report - {orig_name}</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #f7fafc;
            color: #2d3748;
            margin: 0;
            padding: 40px 20px;
            line-height: 1.5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}
        h1 {{
            color: #1a202c;
            font-size: 2.25rem;
            margin-top: 0;
            margin-bottom: 8px;
            border-bottom: 2px solid #edf2f7;
            padding-bottom: 16px;
        }}
        .meta {{
            color: #4a5568;
            margin-bottom: 30px;
            font-size: 0.95rem;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 16px;
        }}
        .report-section {{
            margin-top: 40px;
            border-bottom: 1px solid #edf2f7;
            padding-bottom: 40px;
        }}
        .report-section:last-child {{
            border-bottom: none;
            padding-bottom: 0;
        }}
        h2 {{
            color: #2b6cb0;
            font-size: 1.5rem;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .image-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            background: #f8fafc;
            border: 1px solid #edf2f7;
            border-radius: 8px;
            padding: 16px;
            margin-top: 12px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .badge {{
            background-color: #ebf8ff;
            color: #2b6cb0;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Audio Enhancement Comparison Report</h1>
        <div class="meta">
            <strong>Original File:</strong> {orig_name}<br>
            <strong>Processed File:</strong> {proc_name}<br>
            <strong>Generated On:</strong> {date_str}
        </div>
"""
        for png in generated_pngs:
            # We want to display them nicely using relative path reference
            relative_name = png.name
            if "spectrogram" in relative_name:
                title = "Spectrogram Analysis"
                desc = "Displays frequency magnitude distribution over time. Shows original, processed, and the difference magnitude."
            elif "waveform" in relative_name:
                title = "Waveform Amplitude Analysis"
                desc = "Displays amplitude levels over time. Shows full waveform overlay and a 100ms zoomed-in comparison."
            elif "frequency" in relative_name:
                title = "Power Spectral Density (PSD) Analysis"
                desc = "Displays signal power vs frequency. Shows full spectral distribution comparison and magnitude differences in dB."
            else:
                title = "Report Visual Comparison"
                desc = "Visual analysis comparison report."
                
            html_content += f"""
        <div class="report-section">
            <h2><span class="badge">Visual</span> {title}</h2>
            <p>{desc}</p>
            <div class="image-container">
                <img src="{relative_name}" alt="{title}">
            </div>
        </div>
"""
            
        html_content += """
    </div>
</body>
</html>
"""
        html_path = self.output_dir / f"{stem}_report_summary.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return html_path
        
    @classmethod
    def create_default(cls, output_dir: str = ".reports") -> "ReportGenerator":
        """Factory method to create a generator with all default reports."""
        gen = cls(output_dir)
        gen.add_report(SpectrogramReport(output_dir))
        gen.add_report(WaveformReport(output_dir))
        gen.add_report(FrequencySpectrumReport(output_dir))
        return gen


class ReportBuilder:
    """Builder pattern to compose custom generators and direct output formats."""
    
    def __init__(self, output_dir: str = ".reports"):
        self.output_dir = output_dir
        self.reports_to_add = []
        self.dpi = 150
        
    def add_spectrogram(self) -> "ReportBuilder":
        """Add spectrogram comparison to the build checklist."""
        self.reports_to_add.append("spectrogram")
        return self
        
    def add_waveform(self) -> "ReportBuilder":
        """Add waveform comparison to the build checklist."""
        self.reports_to_add.append("waveform")
        return self
        
    def add_frequency_spectrum(self) -> "ReportBuilder":
        """Add frequency spectrum comparison to the build checklist."""
        self.reports_to_add.append("frequency_spectrum")
        return self
        
    def set_dpi(self, dpi: int) -> "ReportBuilder":
        """Set custom DPI resolution for output images."""
        self.dpi = dpi
        return self
        
    def build(self) -> ReportGenerator:
        """Build and return configured ReportGenerator instance."""
        generator = ReportGenerator(self.output_dir, dpi=self.dpi)
        for r_name in self.reports_to_add:
            report = ReportFactory.create_report(r_name, self.output_dir, dpi=self.dpi)
            generator.add_report(report)
        return generator
