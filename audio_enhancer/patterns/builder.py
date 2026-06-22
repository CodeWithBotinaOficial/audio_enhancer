from typing import List
from pydub import AudioSegment
from .behavioral import AudioProcessingStep

# --- Builder Pattern ---
# Separates the construction of a complex object from its representation,
# so that the same construction process can create different representations.

class Pipeline:
    """Represents a complex audio processing pipeline.

    Maintains a list of processing steps (strategies) and executes them sequentially
    on the input audio segment.
    """
    def __init__(self):
        self._steps: List[AudioProcessingStep] = []

    def add(self, step: AudioProcessingStep):
        """Adds a processing step to the pipeline.

        Args:
            step (AudioProcessingStep): The audio processing strategy to add.
        """
        self._steps.append(step)

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Processes the audio through all steps in the pipeline sequentially.

        Args:
            audio (AudioSegment): The input audio segment to be processed.

        Returns:
            AudioSegment: The fully processed audio segment.
        """
        for step in self._steps:
            audio = step.process(audio)
        return audio

class PipelineBuilder:
    """Builder for creating an audio processing pipeline.

    Provides a fluent API to configure and construct a `Pipeline` instance by
    chaining steps.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets the builder state with a fresh `Pipeline` instance."""
        self._pipeline = Pipeline()

    def add_step(self, step: AudioProcessingStep) -> 'PipelineBuilder':
        """Adds a step to the pipeline being built and returns the builder.

        Args:
            step (AudioProcessingStep): The audio processing strategy to add.

        Returns:
            PipelineBuilder: The current builder instance for method chaining.
        """
        self._pipeline.add(step)
        return self

    def build(self) -> Pipeline:
        """Builds and returns the configured Pipeline, then resets the builder.

        Returns:
            Pipeline: The constructed and ready-to-use audio processing pipeline.
        """
        pipeline = self._pipeline
        self.reset()
        return pipeline
