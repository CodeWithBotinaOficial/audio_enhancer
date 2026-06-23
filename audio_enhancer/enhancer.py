from .audio_loader import load_audio
from .audio_exporter import export_audio
from .patterns.builder import PipelineBuilder
from pydub import AudioSegment

# Facade Pattern: Provides a simplified interface to a library, a framework,
# or any other complex set of classes.

# Singleton Pattern: Ensures a class has only one instance and provides a
# global point of access to it.

class AudioEnhancer:
    """A facade and Singleton for the audio enhancement system.

    Provides a simplified, high-level interface to the underlying audio loading,
    exporting, and pipeline building components.

    Example:
        >>> enhancer = AudioEnhancer.get_instance()
        >>> audio = enhancer.load_audio("input.wav")
        >>> builder = enhancer.get_builder()
        >>> pipeline = builder.add_step(SpectralGatingNoiseReducer()).build()
        >>> enhanced = pipeline.process(audio)
        >>> enhancer.export_audio(enhanced, "output.wav", "wav")
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioEnhancer, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'AudioEnhancer':
        """Provides a global access point to the Singleton instance.

        Returns:
            AudioEnhancer: The active singleton instance.
        """
        return cls()

    def load_audio(self, file_path: str) -> AudioSegment:
        """Loads an audio file from disk into an AudioSegment.

        This hides the detailed loader implementations and formats support.

        Args:
            file_path (str): Path to the input audio file.

        Returns:
            AudioSegment: The loaded pydub AudioSegment.

        Raises:
            FileNotFoundError: If the file does not exist.
            Exception: If pydub or ffmpeg fails to decode the file.
        """
        return load_audio(file_path)

    def export_audio(self, audio: AudioSegment, file_path: str, format: str):
        """Exports an AudioSegment to a file with the specified format.

        This hides the details of the exporter module and formats support.

        Args:
            audio (AudioSegment): The audio segment to export.
            file_path (str): The destination file path.
            format (str): The desired output format (e.g., 'mp3', 'wav', 'flac').

        Raises:
            Exception: If the audio export fails.
        """
        export_audio(audio, file_path, format)

    def get_builder(self) -> PipelineBuilder:
        """Returns a new PipelineBuilder instance.

        Integrates the Builder pattern into the facade to allow chaining steps.

        Returns:
            PipelineBuilder: A new pipeline builder instance.
        """
        return PipelineBuilder()
