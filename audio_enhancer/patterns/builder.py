from typing import List
from pydub import AudioSegment
from .behavioral import AudioProcessingStep

# --- Builder Pattern ---
# Separates the construction of a complex object from its representation,
# so that the same construction process can create different representations.

class Pipeline:
    """Represents a complex audio processing pipeline."""
    def __init__(self):
        self._steps: List[AudioProcessingStep] = []

    def add(self, step: AudioProcessingStep):
        self._steps.append(step)

    def process(self, audio: AudioSegment) -> AudioSegment:
        """Processes the audio through all steps in the pipeline."""
        for step in self._steps:
            audio = step.process(audio)
        return audio

class PipelineBuilder:
    """Builder for creating an audio processing pipeline."""
    def __init__(self):
        self.reset()

    def reset(self):
        self._pipeline = Pipeline()

    def add_step(self, step: AudioProcessingStep) -> 'PipelineBuilder':
        self._pipeline.add(step)
        return self

    def build(self) -> Pipeline:
        pipeline = self._pipeline
        self.reset()
        return pipeline
