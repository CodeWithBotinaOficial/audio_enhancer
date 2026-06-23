from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

class BaseReport(ABC):
    """Abstract base class for all audio comparison reports."""
    
    def __init__(self, output_dir: Any, dpi: int = 150, figsize: tuple = (14, 6)):
        self.output_dir = Path(output_dir)
        self.dpi = dpi
        self.figsize = figsize
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def generate(self, original_audio: Any, processed_audio: Any, 
                 original_path: Path, processed_path: Path) -> Path:
        """
        Generate the report and return the path to the saved file.
        
        Args:
            original_audio: The original audio data (numpy array or AudioSegment).
            processed_audio: The processed audio data.
            original_path: Path to the original file.
            processed_path: Path to the processed file.
        
        Returns:
            Path to the generated report file.
        """
        pass
    
    @property
    @abstractmethod
    def report_name(self) -> str:
        """Human-readable name of the report type."""
        pass
