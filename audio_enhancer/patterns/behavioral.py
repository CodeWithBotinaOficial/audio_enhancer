from __future__ import annotations
from abc import ABC, abstractmethod
from pydub import AudioSegment
from typing import Any, List

# --- Strategy Pattern ---
# Lets you define a family of algorithms, put each of them into a separate class,
# and make their objects interchangeable.

class AudioProcessingStep(ABC):
    """Strategy: Interface for an audio processing algorithm."""
    @abstractmethod
    def process(self, audio: AudioSegment) -> AudioSegment:
        pass

# --- Chain of Responsibility Pattern ---
# Lets you pass requests along a chain of handlers. Upon receiving a request,
# each handler decides either to process the request or to pass it to the next handler in the chain.

class Handler(ABC):
    """Abstract Handler"""
    _next_handler: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Any) -> Any:
        if self._next_handler:
            return self._next_handler.handle(request)
        return None

class AudioProcessingHandler(Handler):
    """Concrete handler for processing audio with a specific step."""
    def __init__(self, processor: AudioProcessingStep):
        self._processor = processor

    def handle(self, audio: AudioSegment) -> AudioSegment:
        processed_audio = self._processor.process(audio)
        # Pass to the next handler
        super().handle(processed_audio)
        return processed_audio

# --- Command Pattern ---
# Turns a request into a stand-alone object that contains all information about the request.

class Command(ABC):
    """Command interface"""
    @abstractmethod
    def execute(self) -> Any:
        pass

class EnhanceAudioCommand(Command):
    """Concrete command to execute the enhancement pipeline."""
    def __init__(self, receiver: 'AudioEnhancer', audio_path: str, pipeline: 'Pipeline'):
        self._receiver = receiver
        self._audio_path = audio_path
        self._pipeline = pipeline

    def execute(self) -> AudioSegment:
        audio = self._receiver.load_audio(self._audio_path)
        return self._pipeline.process(audio)

# --- Observer Pattern ---
# Lets you define a subscription mechanism to notify multiple objects
# about any events that happen to the object they’re observing.

class EventListener(ABC):
    """Observer interface"""
    @abstractmethod
    def update(self, event_type: str, data: Any):
        pass

class EventManager:
    """Subject (or Publisher)"""
    def __init__(self):
        self._listeners: List[EventListener] = []

    def subscribe(self, listener: EventListener):
        self._listeners.append(listener)

    def unsubscribe(self, listener: EventListener):
        self._listeners.remove(listener)

    def notify(self, event_type: str, data: Any):
        for listener in self._listeners:
            listener.update(event_type, data)

class LoggingListener(EventListener):
    """Concrete observer that logs events."""
    def update(self, event_type: str, data: Any):
        from audio_enhancer.utils.logger import logger
        logger.info(f"Event '{event_type}' with data: {data}")

# --- State Pattern ---
# Lets an object alter its behavior when its internal state changes.

class AudioFileState(ABC):
    """State interface"""
    def __init__(self, context: 'AudioFileContext'):
        self._context = context

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def save(self):
        pass

class RawState(AudioFileState):
    """Concrete state for raw, unprocessed audio."""
    def process(self):
        print("Processing audio...")
        # Actual processing logic would be here
        self._context.state = ProcessedState(self._context)

    def save(self):
        print("Cannot save raw audio. Process it first.")

class ProcessedState(AudioFileState):
    """Concrete state for processed audio."""
    def process(self):
        print("Audio is already processed.")

    def save(self):
        print("Saving processed audio...")
        self._context.state = SavedState(self._context)

class SavedState(AudioFileState):
    """Concrete state for saved audio."""
    def process(self):
        print("Cannot process saved audio. Load a new file.")

    def save(self):
        print("Audio is already saved.")

class AudioFileContext:
    """Context class that holds the state."""
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.state: AudioFileState = RawState(self)

    def request_process(self):
        self.state.process()

    def request_save(self):
        self.state.save()

# --- Mediator Pattern ---
# Lets you reduce chaotic dependencies between objects. The pattern restricts
# direct communications between the objects and forces them to collaborate only
# via a mediator object.

class AudioMediator(ABC):
    """Mediator interface"""
    @abstractmethod
    def notify(self, sender: object, event: str):
        pass

class EnhancementMediator(AudioMediator):
    """Concrete mediator for coordinating audio enhancement components."""
    def __init__(self, loader: 'AudioLoader', exporter: 'AudioExporter', pipeline: 'Pipeline'):
        self._loader = loader
        self._exporter = exporter
        self._pipeline = pipeline
        # In a real app, these components would have a reference to the mediator

    def notify(self, sender: object, event: str):
        if event == 'load':
            print("Mediator: Load event detected. Notifying pipeline.")
        elif event == 'process':
            print("Mediator: Process event detected. Notifying exporter.")
