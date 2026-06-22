import os
from click.testing import CliRunner
from cli import cli
from examples.demo import main as create_sample_file

def test_cli_process_file():
    # Create a sample file to process
    create_sample_file()
    input_file = "examples/sample_audio/input.m4a"
    output_file = "examples/output/cli_test_output.wav"

    runner = CliRunner()
    result = runner.invoke(cli, [
        'process-file',
        input_file,
        output_file,
        '--noise-profile', 'spectral_gate',
        '--normalize', 'lufs',
        '--lufs', '-14'
    ])

    assert result.exit_code == 0
    assert os.path.exists(output_file)
    assert "Processed" in result.output

    # Clean up the created file
    if os.path.exists(output_file):
        os.remove(output_file)
