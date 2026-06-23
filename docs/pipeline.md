# Pipeline Builder

This section covers the `PipelineBuilder` interface, pipeline mechanics, and how to create custom audio processors.

## Chaining Processors

The `PipelineBuilder` uses the **Builder Pattern** to construct a `Pipeline` instance step-by-step. It provides a fluent, method-chaining API where `add_step` returns the builder instance itself, letting you assemble pipelines concisely:

```python
pipeline = (
    enhancer.get_builder()
    .add_step(SpectralGatingNoiseReducer())
    .add_step(ImpulseNoiseReducer())
    .add_step(LufsNormalizer(-16.0))
    .build()
)
```

---

## Under the Hood: Pipeline execution

When you call `pipeline.process(audio)`, the `Pipeline` class iterates over the registered `AudioProcessingStep` list and applies each processor sequentially. 

Each step's `.process()` method consumes a `pydub.AudioSegment`, executes its algorithms, and returns a new `pydub.AudioSegment`, which is then passed to the next step.

---

## Adding Custom Steps

You can easily extend the library by creating your own custom processing steps. To do this, implement the `AudioProcessingStep` abstract interface:

### 1. Define the Step

Subclass `AudioProcessingStep` and implement the abstract `process` method:

```python
from audio_enhancer import AudioProcessingStep
from pydub import AudioSegment

class CustomHighPassFilter(AudioProcessingStep):
    """Custom step that applies a high-pass filter to the audio segment."""
    def __init__(self, cutoff_frequency: int = 150):
        self.cutoff_frequency = cutoff_frequency

    def process(self, audio: AudioSegment) -> AudioSegment:
        print(f"Applying high-pass filter at {self.cutoff_frequency} Hz...")
        return audio.high_pass_filter(self.cutoff_frequency)
```

### 2. Register and Run

Once defined, pass your custom class instance directly to `add_step()`:

```python
pipeline = (
    enhancer.get_builder()
    .add_step(CustomHighPassFilter(cutoff_frequency=120))
    .add_step(LufsNormalizer(-16.0))
    .build()
)

processed_audio = pipeline.process(audio)
```
