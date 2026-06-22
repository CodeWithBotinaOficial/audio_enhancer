import click
from audio_enhancer.enhancer import AudioEnhancer
from audio_enhancer.normalization.lufs import LufsNormalizer
from audio_enhancer.normalization.peak import PeakNormalizer
from audio_enhancer.normalization.rms import RmsNormalizer
from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
from audio_enhancer.noise_reduction.impulse_noise import ImpulseNoiseReducer

@click.group()
def cli():
    """A command-line tool for audio enhancement."""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--noise-profile', type=click.Choice(['spectral_gate', 'impulse', 'none']), default='none', help='Noise reduction profile.')
@click.option('--normalize', type=click.Choice(['peak', 'rms', 'lufs', 'none']), default='none', help='Normalization method.')
@click.option('--lufs', type=float, default=-16.0, help='Target LUFS for normalization.')
@click.option('--peak-db', type=float, default=-1.0, help='Target peak dBFS for normalization.')
@click.option('--rms-db', type=float, default=-20.0, help='Target RMS dBFS for normalization.')
def process_file(input_file, output_file, noise_profile, normalize, lufs, peak_db, rms_db):
    """Process a single audio file."""
    enhancer = AudioEnhancer.get_instance()
    builder = enhancer.get_builder()

    # Add noise reduction step
    if noise_profile == 'spectral_gate':
        builder.add_step(SpectralGatingNoiseReducer())
    elif noise_profile == 'impulse':
        builder.add_step(ImpulseNoiseReducer())

    # Add normalization step
    if normalize == 'lufs':
        builder.add_step(LufsNormalizer(lufs))
    elif normalize == 'peak':
        builder.add_step(PeakNormalizer(peak_db))
    elif normalize == 'rms':
        builder.add_step(RmsNormalizer(rms_db))

    pipeline = builder.build()

    # Load audio
    audio = enhancer.load_audio(input_file)

    # Process audio
    if pipeline._steps:
        processed_audio = pipeline.process(audio)
    else:
        processed_audio = audio

    # Export audio
    output_format = output_file.split('.')[-1]
    enhancer.export_audio(processed_audio, output_file, output_format)

    click.echo(f"Processed {input_file} and saved to {output_file}")

if __name__ == '__main__':
    cli()
