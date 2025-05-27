"""
VidGen core components

This package contains core functionality that's used throughout the application:
- Configuration settings
- Custom exceptions
"""

from vidgen.core.config import VideoGenConfig
from vidgen.core.exceptions import (
    VidGenException,
    ScriptParsingError,
    ModelLoadError,
    AudioGenerationError,
    ImageGenerationError,
    VideoAssemblyError,
    ConfigurationError
)
