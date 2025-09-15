from abc import ABC, abstractmethod
from .structural import NoiseReducer, Normalizer

# --- Factory Method Pattern ---
# Defines an interface for creating an object, but lets subclasses alter the type of objects that will be created.

class AudioProcessorFactory(ABC):
    """Abstract factory for creating audio processors."""
    @abstractmethod
    def create_processor(self) -> 'AudioProcessor':
        pass

class NoiseReducerFactory(AudioProcessorFactory):
    def __init__(self, strategy: str):
        self._strategy = strategy

    def create_processor(self) -> NoiseReducer:
        # This is a simplified factory method.
        # In a real-world scenario, this could involve more complex object creation.
        if self._strategy == 'spectral_gate':
            from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
            return SpectralGatingNoiseReducer()
        elif self._strategy == 'impulse':
            from audio_enhancer.noise_reduction.impulse_noise import ImpulseNoiseReducer
            return ImpulseNoiseReducer()
        else:
            raise ValueError(f"Unknown noise reduction strategy: {self._strategy}")

# --- Abstract Factory Pattern ---
# Provides an interface for creating families of related or dependent objects without specifying their concrete classes.

class EnhancementFactory(ABC):
    """Abstract factory for creating families of enhancement tools."""
    @abstractmethod
    def create_noise_reducer(self) -> NoiseReducer:
        pass

    @abstractmethod
    def create_normalizer(self) -> Normalizer:
        pass

class BasicEnhancementFactory(EnhancementFactory):
    """Factory for creating basic, fast enhancement tools."""
    def create_noise_reducer(self) -> NoiseReducer:
        from audio_enhancer.noise_reduction.spectral_gating import SpectralGatingNoiseReducer
        return SpectralGatingNoiseReducer()

    def create_normalizer(self) -> Normalizer:
        from audio_enhancer.normalization.peak import PeakNormalizer
        return PeakNormalizer()

class ProEnhancementFactory(EnhancementFactory):
    """Factory for creating high-quality, but potentially slower, enhancement tools."""
    def create_noise_reducer(self) -> NoiseReducer:
        # In a real app, this could be a more advanced algorithm
        from audio_enhancer.noise_reduction.impulse_noise import ImpulseNoiseReducer
        return ImpulseNoiseReducer()

    def create_normalizer(self) -> Normalizer:
        from audio_enhancer.normalization.lufs import LufsNormalizer
        return LufsNormalizer(-14.0) # Target LUFS for professional audio
