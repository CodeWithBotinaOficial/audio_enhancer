import os
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import numpy as np

from audio_enhancer.reports import BaseReport
from audio_enhancer.reports.generator import ReportGenerator, ReportBuilder, ReportFactory
from audio_enhancer.reports.spectrogram import SpectrogramReport
from audio_enhancer.reports.waveform import WaveformReport
from audio_enhancer.reports.frequency_spectrum import FrequencySpectrumReport


class TestReportGenerator:
    def test_create_default_returns_generator_with_all_reports(self, tmp_path):
        gen = ReportGenerator.create_default(str(tmp_path / ".reports"))
        assert len(gen._reports) == 3
        assert any(isinstance(r, SpectrogramReport) for r in gen._reports)
        assert any(isinstance(r, WaveformReport) for r in gen._reports)
        assert any(isinstance(r, FrequencySpectrumReport) for r in gen._reports)
    
    def test_add_report_returns_self_for_chaining(self, tmp_path):
        gen = ReportGenerator(str(tmp_path / ".reports"))
        result = gen.add_report(Mock(spec=SpectrogramReport))
        assert result is gen
    
    @patch("audio_enhancer.reports.generator.get_audio_data")
    @patch("audio_enhancer.reports.generator.ReportGenerator._compile_html_summary")
    def test_generate_all_calls_each_report(self, mock_compile, mock_get_data, tmp_path):
        mock_get_data.return_value = (np.zeros(1000), 44100)
        mock_compile.return_value = tmp_path / "summary.html"
        
        report_mock = Mock(spec=SpectrogramReport)
        report_mock.generate.return_value = tmp_path / "test.png"
        
        gen = ReportGenerator(str(tmp_path / ".reports"))
        gen.add_report(report_mock)
        
        paths = gen.generate_all("input.wav", "output.wav")
        
        assert len(paths) == 2  # png + html
        report_mock.generate.assert_called_once()
        mock_compile.assert_called_once()
    
    def test_output_dir_created_if_not_exists(self, tmp_path):
        reports_dir = tmp_path / "new_reports"
        assert not reports_dir.exists()
        ReportGenerator(str(reports_dir))
        assert reports_dir.exists()


class TestSpectrogramReport:
    @patch("audio_enhancer.reports.spectrogram.get_audio_data")
    @patch("audio_enhancer.reports.spectrogram.save_figure")
    def test_generate_creates_spectrogram_file(self, mock_save_figure, mock_get_data, tmp_path):
        mock_get_data.return_value = (np.random.randn(44100), 44100)
        
        report = SpectrogramReport(tmp_path / "reports")
        result = report.generate(
            np.random.randn(44100), np.random.randn(44100),
            Path("input.wav"), Path("output.wav")
        )
        
        assert result.suffix == ".png"
        assert "spectrogram" in result.name
        mock_save_figure.assert_called_once()


class TestWaveformReport:
    @patch("audio_enhancer.reports.waveform.get_audio_data")
    @patch("audio_enhancer.reports.waveform.save_figure")
    def test_generate_creates_waveform_file(self, mock_save_figure, mock_get_data, tmp_path):
        mock_get_data.return_value = (np.random.randn(44100), 44100)
        
        report = WaveformReport(tmp_path / "reports")
        result = report.generate(
            np.random.randn(44100), np.random.randn(44100),
            Path("input.wav"), Path("output.wav")
        )
        
        assert result.suffix == ".png"
        assert "waveform" in result.name
        mock_save_figure.assert_called_once()


class TestFrequencySpectrumReport:
    @patch("audio_enhancer.reports.frequency_spectrum.get_audio_data")
    @patch("audio_enhancer.reports.frequency_spectrum.save_figure")
    def test_generate_creates_spectrum_file(self, mock_save_figure, mock_get_data, tmp_path):
        mock_get_data.return_value = (np.random.randn(44100), 44100)
        
        report = FrequencySpectrumReport(tmp_path / "reports")
        result = report.generate(
            np.random.randn(44100), np.random.randn(44100),
            Path("input.wav"), Path("output.wav")
        )
        
        assert result.suffix == ".png"
        assert "frequency" in result.name
        mock_save_figure.assert_called_once()


class TestReportFactory:
    def test_creates_correct_report_types(self, tmp_path):
        out = tmp_path / "factory_out"
        
        r1 = ReportFactory.create_report("spectrogram", out)
        assert isinstance(r1, SpectrogramReport)
        
        r2 = ReportFactory.create_report("waveform", out)
        assert isinstance(r2, WaveformReport)
        
        r3 = ReportFactory.create_report("frequency_spectrum", out)
        assert isinstance(r3, FrequencySpectrumReport)
        
        r4 = ReportFactory.create_report("frequency", out)
        assert isinstance(r4, FrequencySpectrumReport)
        
    def test_raises_value_error_for_unknown_report_type(self, tmp_path):
        with pytest.raises(ValueError, match="Unknown report type"):
            ReportFactory.create_report("nonexistent_report_type", tmp_path)


class TestBaseReportInstantiation:
    def test_cannot_instantiate_base_report_directly(self, tmp_path):
        with pytest.raises(TypeError):
            BaseReport(tmp_path)


class TestReportBuilder:
    def test_builder_constructs_configured_generator(self, tmp_path):
        out = tmp_path / "builder_out"
        gen = (
            ReportBuilder(str(out))
            .add_spectrogram()
            .add_waveform()
            .add_frequency_spectrum()
            .set_dpi(250)
            .build()
        )
        assert len(gen._reports) == 3
        assert gen.dpi == 250
        assert gen.output_dir == out


class TestCLIReportFlag:
    @patch("audio_enhancer.reports.generator.ReportGenerator.generate_all")
    def test_cli_process_file_with_report_flag(self, mock_generate_all, tmp_path):
        from click.testing import CliRunner
        from audio_enhancer.cli import cli
        from examples.demo import main as create_sample_file
        
        create_sample_file()
        input_file = "examples/sample_audio/input.m4a"
        output_file = str(tmp_path / "cli_test_output.wav")
        mock_generate_all.return_value = [Path("dummy.png"), Path("dummy.html")]
        
        runner = CliRunner()
        result = runner.invoke(cli, [
            'process-file',
            input_file,
            output_file,
            '--generate-report',
            '--report-dpi', '120'
        ])
        
        assert result.exit_code == 0
        mock_generate_all.assert_called_once_with(input_file, output_file)
        
        # Verify output message contains visual report log info
        assert "Generating visual comparison reports..." in result.output
        assert "dummy.png" in result.output
        assert "dummy.html" in result.output

    def test_reports_directory_created_in_cwd(self, tmp_path):
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Running CLI command with report triggers the creation of directory .reports
            from click.testing import CliRunner
            from audio_enhancer.cli import cli
            from examples.demo import main as create_sample_file
            
            # Use real runner context to ensure .reports is created in CWD
            # Mock generate_all to avoid actual plotting during verification
            with patch("audio_enhancer.reports.generator.ReportGenerator.generate_all") as mock_gen_all:
                mock_gen_all.return_value = []
                create_sample_file()
                input_file = os.path.join(old_cwd, "examples/sample_audio/input.m4a")
                output_file = str(tmp_path / "cli_out.wav")
                
                runner = CliRunner()
                runner.invoke(cli, [
                    'process-file',
                    input_file,
                    output_file,
                    '--generate-report'
                ])
                
                assert os.path.exists(".reports")
        finally:
            os.chdir(old_cwd)
