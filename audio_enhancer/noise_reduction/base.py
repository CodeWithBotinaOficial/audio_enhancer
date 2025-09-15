from pydub import AudioSegment
from ..patterns.behavioral import AudioProcessingStep

class NoiseReductionStrategy(AudioProcessingStep):
    """Base class for all noise reduction strategies."""
    def process(self, audio: AudioSegment) -> AudioSegment:
        raise NotImplementedError
