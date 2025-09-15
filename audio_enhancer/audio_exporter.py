from pydub import AudioSegment
from audio_enhancer.utils.logger import logger

def export_audio(audio: AudioSegment, file_path: str, format: str):
    """Exports an AudioSegment to a file.

    Args:
        audio: The AudioSegment to export.
        file_path: The path to save the file to.
        format: The desired output format (e.g., 'mp3', 'wav', 'flac').
    """
    logger.info(f"Exporting audio to: {file_path} in format: {format}")
    try:
        # DSD export requires external tools and is not directly supported by pydub.
        # We document this limitation as requested.
        if format.lower() == 'dsd':
            logger.warning("DSD export is not directly supported. This will export as WAV.")
            logger.warning("To convert to DSD, use a tool like FFmpeg: `ffmpeg -i input.wav output.dsf`")
            format = 'wav' # Fallback to WAV

        audio.export(file_path, format=format)
    except Exception as e:
        logger.error(f"Could not export audio file {file_path}: {e}")
        raise
