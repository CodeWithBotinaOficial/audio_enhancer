from .audio_loader import load_audio
from .audio_exporter import export_audio
from .patterns.builder import PipelineBuilder
from pydub import AudioSegment

# Facade Pattern: Provides a simplified interface to a library, a framework,
# or any other complex set of classes.

# Singleton Pattern: Ensures a class has only one instance and provides a
# global point of access to it.

class AudioEnhancer:
    """A facade for the audio enhancement system."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioEnhancer, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'AudioEnhancer':
        """Provides a global access point to the Singleton instance."""
        return cls()

    def load_audio(self, file_path: str) -> AudioSegment:
        """Loads an audio file.
        This is part of the facade, hiding the details of the audio_loader module.
        """
        return load_audio(file_path)

    def export_audio(self, audio: AudioSegment, file_path: str, format: str):
        """Exports an audio file.
        This is part of the facade, hiding the details of the audio_exporter module.
        """
        export_audio(audio, file_path, format)

    def get_builder(self) -> PipelineBuilder:
        """Returns a pipeline builder for creating enhancement pipelines.
        This integrates the Builder pattern into the facade.
        """
        return PipelineBuilder()
