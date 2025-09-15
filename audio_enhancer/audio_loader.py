from pydub import AudioSegment
from audio_enhancer.utils.logger import logger

def load_audio(file_path: str) -> AudioSegment:
    """Loads an audio file from the given path.

    This function uses pydub, which internally uses ffmpeg, so it supports
    a wide variety of audio formats.
    """
    logger.info(f"Loading audio from: {file_path}")
    try:
        return AudioSegment.from_file(file_path)
    except Exception as e:
        logger.error(f"Could not load audio file {file_path}: {e}")
        raise
