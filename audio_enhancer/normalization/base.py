from pydub import AudioSegment
from ..patterns.behavioral import AudioProcessingStep

class NormalizationStrategy(AudioProcessingStep):
    """Base class for all normalization strategies."""
    def process(self, audio: AudioSegment) -> AudioSegment:
        raise NotImplementedError
