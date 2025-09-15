from abc import ABC, abstractmethod
from pydub import AudioSegment
from typing import Dict

# --- Base Interfaces for Structural Patterns ---

class AudioProcessor(ABC):
    """Abstract base class for any audio processing unit."""
    @abstractmethod
    def process(self, audio: AudioSegment) -> AudioSegment:
        pass

class Normalizer(AudioProcessor):
    """Interface for normalization strategies."""
    pass

class NoiseReducer(AudioProcessor):
    """Interface for noise reduction strategies."""
    pass

# --- Adapter Pattern ---
# Allows objects with incompatible interfaces to collaborate.
# We adapt the `pyloudnorm` library to our `Normalizer` interface.

class LoudnessAdapter(Normalizer):
    """Adapter for the pyloudnorm library."""
    def __init__(self, target_lufs: float):
        self._target_lufs = target_lufs
        # The actual pyloudnorm object is created and used in the `process` method.

    def process(self, audio: AudioSegment) -> AudioSegment:
        # This is where the adaptation happens.
        # We convert pydub AudioSegment to a numpy array for pyloudnorm,
        # then convert it back.
        from ..normalization.lufs import LufsNormalizer
        lufs_normalizer = LufsNormalizer(self._target_lufs)
        return lufs_normalizer.process(audio)

# --- Bridge Pattern ---
# Decouples an abstraction from its implementation so the two can vary independently.

class AudioTrack:
    """Abstraction: Represents an audio track that can be played or processed."""
    def __init__(self, implementation: 'AudioImplementation'):
        self._implementation = implementation

    def process(self, effect: AudioProcessor) -> 'AudioTrack':
        processed_data = self._implementation.apply_effect(effect)
        return AudioTrack(processed_data)

    def get_audio_segment(self) -> AudioSegment:
        return self._implementation.get_segment()

class AudioImplementation(ABC):
    """Implementation: Defines the interface for audio data representation."""
    @abstractmethod
    def apply_effect(self, effect: AudioProcessor) -> 'AudioImplementation':
        pass

    @abstractmethod
    def get_segment(self) -> AudioSegment:
        pass

class PydubImplementation(AudioImplementation):
    """Concrete Implementation: Uses pydub to handle audio data."""
    def __init__(self, audio: AudioSegment):
        self._audio = audio

    def apply_effect(self, effect: AudioProcessor) -> 'AudioImplementation':
        processed_audio = effect.process(self._audio)
        return PydubImplementation(processed_audio)

    def get_segment(self) -> AudioSegment:
        return self._audio

# --- Composite Pattern ---
# Lets you compose objects into tree structures and then work with these
# structures as if they were individual objects.

class AudioComponent(AudioProcessor):
    """Component: Base interface for both individual effects and composite pipelines."""
    def add(self, component: 'AudioComponent'):
        raise NotImplementedError

    def remove(self, component: 'AudioComponent'):
        raise NotImplementedError

class Effect(AudioComponent):
    """Leaf: A single audio effect."""
    def __init__(self, processor: AudioProcessor):
        self._processor = processor

    def process(self, audio: AudioSegment) -> AudioSegment:
        return self._processor.process(audio)

class Pipeline(AudioComponent):
    """Composite: A collection of audio components."""
    def __init__(self):
        self._children: list[AudioComponent] = []

    def add(self, component: AudioComponent):
        self._children.append(component)

    def remove(self, component: AudioComponent):
        self._children.remove(component)

    def process(self, audio: AudioSegment) -> AudioSegment:
        for component in self._children:
            audio = component.process(audio)
        return audio

# --- Decorator Pattern ---
# Attaches new behaviors to objects by placing these objects inside special
# wrapper objects that contain the behaviors.

class AudioDecorator(AudioProcessor):
    """Decorator: Wraps an audio processor to add functionality."""
    def __init__(self, wrapped: AudioProcessor):
        self._wrapped = wrapped

    def process(self, audio: AudioSegment) -> AudioSegment:
        return self._wrapped.process(audio)

class FadeInDecorator(AudioDecorator):
    """Concrete Decorator: Adds a fade-in effect."""
    def __init__(self, wrapped: AudioProcessor, duration: int):
        super().__init__(wrapped)
        self._duration = duration

    def process(self, audio: AudioSegment) -> AudioSegment:
        processed_audio = self._wrapped.process(audio)
        return processed_audio.fade_in(self._duration)

# --- Proxy Pattern ---
# Provides a surrogate or placeholder for another object to control access to it.

class LazyAudioLoader:
    """Proxy: A proxy for loading a large audio file."""
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._audio_segment: AudioSegment | None = None

    def get_audio(self) -> AudioSegment:
        if self._audio_segment is None:
            from ..audio_loader import load_audio
            self._audio_segment = load_audio(self._file_path)
        return self._audio_segment

# --- Flyweight Pattern ---
# Lets you fit more objects into the available amount of RAM by sharing
# common parts of state between multiple objects instead of keeping all
# the data in each object.

class AudioEffectFlyweight:
    """The Flyweight stores a common portion of the state (intrinsic state)
    that belongs to multiple real business entities."""
    def __init__(self, effect_name: str):
        self._effect_name = effect_name
        # In a real app, this would be a pre-configured, heavy object
        print(f"Creating a new flyweight for: {self._effect_name}")

    def apply(self, audio: AudioSegment, settings: Dict) -> AudioSegment:
        # The extrinsic state (settings) is passed to the flyweight's method.
        print(f"Applying {self._effect_name} with settings: {settings}")
        # Dummy processing
        return audio

class FlyweightFactory:
    """The Flyweight Factory creates and manages the flyweight objects."""
    _flyweights: Dict[str, AudioEffectFlyweight] = {}

    def get_flyweight(self, effect_name: str) -> AudioEffectFlyweight:
        if effect_name not in self._flyweights:
            self._flyweights[effect_name] = AudioEffectFlyweight(effect_name)
        return self._flyweights[effect_name]
