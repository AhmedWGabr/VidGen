# VidGen API Reference

This document provides comprehensive API documentation for VidGen's core modules and classes.

## Table of Contents

- [Core Configuration](#core-configuration)
- [Error Handling](#error-handling)
- [Audio Models](#audio-models)
- [Video Models](#video-models)
- [Image Models](#image-models)
- [Text-to-Speech](#text-to-speech)
- [Services](#services)
- [Utilities](#utilities)

## Core Configuration

### Config Class

The main configuration class for VidGen settings.

```python
from src.vidgen.core.config import Config

config = Config()
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `GEMINI_API_KEY` | str | None | API key for Gemini integration |
| `HUGGINGFACE_TOKEN` | str | None | HuggingFace authentication token |
| `IMAGE_MODEL` | str | "stabilityai/stable-diffusion-xl-base-1.0" | Stable Diffusion model |
| `TTS_MODEL` | str | "bark" | Text-to-speech model |
| `VIDEO_RESOLUTION` | tuple | (1920, 1080) | Output video resolution |
| `VIDEO_FPS` | int | 30 | Video frame rate |
| `DEFAULT_SEGMENT_DURATION` | float | 5.0 | Default segment duration in seconds |
| `AUDIO_SAMPLE_RATE` | int | 44100 | Audio sample rate |
| `AUDIO_CHANNELS` | int | 2 | Audio channel count |

#### Methods

```python
def get_output_dir() -> str:
    """Get the configured output directory."""

def get_temp_dir() -> str:
    """Get the temporary files directory."""

def validate() -> bool:
    """Validate configuration settings."""
```

## Error Handling

### Exception Classes

#### VidGenError

Base exception class for all VidGen errors.

```python
from src.vidgen.core.exceptions import VidGenError

class VidGenError(Exception):
    def __init__(self, message: str, original_exception: Exception = None, 
                 recovery_suggestion: str = None):
        self.original_exception = original_exception
        self.recovery_suggestion = recovery_suggestion
```

#### Specialized Exceptions

- `FFmpegError` - FFmpeg processing errors
- `APIError` - External API errors
- `FileSystemError` - File system operation errors
- `MemoryError` - Memory allocation errors
- `DependencyError` - Missing dependency errors

### Error Recovery

#### @with_error_recovery Decorator

Automatically handles errors with recovery suggestions.

```python
from src.vidgen.core.exceptions import with_error_recovery

@with_error_recovery
def my_function():
    # Function implementation
    pass
```

#### ErrorRecovery Class

```python
from src.vidgen.core.exceptions import ErrorRecovery

recovery = ErrorRecovery()
user_message = recovery.get_user_friendly_message(exception)
suggestion = recovery.get_recovery_suggestion(exception)
```

## Audio Models

### AudioModel Class

Advanced audio generation and processing capabilities.

```python
from src.vidgen.models.audio import AudioModel

audio_model = AudioModel(config)
```

#### Methods

##### generate_audio()

Generate audio based on text description.

```python
def generate_audio(self, command: str, duration: float = None, 
                   output_path: str = None) -> str:
    """
    Generate audio based on command description.
    
    Args:
        command: Text description of desired audio
        duration: Duration in seconds (auto-detected if None)
        output_path: Output file path (auto-generated if None)
    
    Returns:
        Path to generated audio file
    
    Examples:
        # Generate silence
        audio_model.generate_audio("silence for 10 seconds")
        
        # Generate ambient sounds
        audio_model.generate_audio("peaceful forest ambient sounds")
        
        # Generate music
        audio_model.generate_audio("upbeat electronic music in C major")
    """
```

##### mix_audio()

Mix multiple audio tracks.

```python
def mix_audio(self, audio_paths: List[str], volumes: List[float] = None,
              output_path: str = None) -> str:
    """
    Mix multiple audio tracks.
    
    Args:
        audio_paths: List of input audio file paths
        volumes: Volume levels (0.0-1.0) for each track
        output_path: Output file path
    
    Returns:
        Path to mixed audio file
    """
```

#### Private Methods

- `_analyze_audio_command()` - Analyze command to determine audio type
- `_generate_silence()` - Generate silence
- `_generate_ambient_audio()` - Generate ambient sounds
- `_generate_music_audio()` - Generate musical content
- `_extract_duration()` - Extract duration from text
- `_get_frequency_pattern()` - Get frequency pattern for audio type

## Video Models

### VideoModel Class

Video generation, effects, and post-processing.

```python
from src.vidgen.models.video import VideoModel

video_model = VideoModel(config)
```

#### Methods

##### generate_video_with_transitions()

Create video with professional transitions between segments.

```python
def generate_video_with_transitions(self, image_paths: List[str], 
                                   audio_path: str, 
                                   transition_type: str = "fade",
                                   segment_duration: float = 5.0,
                                   output_path: str = None) -> str:
    """
    Generate video with transitions between image segments.
    
    Args:
        image_paths: List of image file paths
        audio_path: Audio file path
        transition_type: Type of transition ("fade", "slide_left", "slide_right", "wipe")
        segment_duration: Duration of each segment in seconds
        output_path: Output video file path
    
    Returns:
        Path to generated video file
    """
```

##### add_motion_effects()

Add motion effects to existing video.

```python
def add_motion_effects(self, video_path: str, effect_type: str,
                      intensity: float = 0.2, output_path: str = None) -> str:
    """
    Add motion effects to video.
    
    Args:
        video_path: Input video file path
        effect_type: Effect type ("zoom_pan", "parallax", "shake")
        intensity: Effect intensity (0.0-1.0)
        output_path: Output video file path
    
    Returns:
        Path to processed video file
    """
```

##### create_multi_angle_video()

Create video with multiple camera angles.

```python
def create_multi_angle_video(self, base_video_path: str, 
                           angles: List[str] = None,
                           switch_interval: float = 3.0,
                           output_path: str = None) -> str:
    """
    Create multi-angle video effect.
    
    Args:
        base_video_path: Base video file path
        angles: List of angle effects to apply
        switch_interval: Time between angle switches
        output_path: Output video file path
    
    Returns:
        Path to multi-angle video
    """
```

##### concatenate_videos()

Combine multiple video segments.

```python
def concatenate_videos(self, video_paths: List[str], 
                      output_path: str = None) -> str:
    """
    Concatenate multiple video files.
    
    Args:
        video_paths: List of video file paths to concatenate
        output_path: Output video file path
    
    Returns:
        Path to concatenated video
    """
```

## Image Models

### ImageModel Class

AI-powered image generation using Stable Diffusion.

```python
from src.vidgen.models.image import ImageModel

image_model = ImageModel(config)
```

#### Methods

##### generate_image()

Generate image from text prompt.

```python
def generate_image(self, prompt: str, negative_prompt: str = None,
                  character: dict = None, output_path: str = None) -> str:
    """
    Generate image using Stable Diffusion.
    
    Args:
        prompt: Text description of desired image
        negative_prompt: Things to avoid in image
        character: Character consistency information
        output_path: Output image file path
    
    Returns:
        Path to generated image file
    """
```

## Text-to-Speech

### TTSModel Class

High-quality text-to-speech using Bark.

```python
from src.vidgen.models.tts import TTSModel

tts_model = TTSModel(config)
```

#### Methods

##### generate_speech()

Convert text to speech.

```python
def generate_speech(self, text: str, voice: str = None,
                   output_path: str = None) -> str:
    """
    Generate speech from text.
    
    Args:
        text: Text to convert to speech
        voice: Voice preset to use
        output_path: Output audio file path
    
    Returns:
        Path to generated speech file
    """
```

## Services

### VideoGenerator Class

Main orchestrator for the video generation pipeline.

```python
from src.vidgen.services.video_generator import VideoGenerator

generator = VideoGenerator(config)
```

#### Methods

##### generate_video()

Generate complete video from script.

```python
def generate_video(self, script: str, output_path: str = None,
                  progress_callback: callable = None,
                  **kwargs) -> str:
    """
    Generate complete video from script.
    
    Args:
        script: Input script text
        output_path: Output video file path
        progress_callback: Progress callback function
        **kwargs: Additional generation options
    
    Returns:
        Path to generated video file
    """
```

### ScriptParser Class

Advanced script analysis and segmentation.

```python
from src.vidgen.services.script_parser import ScriptParser

parser = ScriptParser(config)
```

#### Methods

##### parse_script()

Parse and segment script into video segments.

```python
def parse_script(self, script: str) -> List[dict]:
    """
    Parse script into structured segments.
    
    Args:
        script: Raw script text
    
    Returns:
        List of script segments with metadata
    """
```

## Utilities

### FileManager Class

File system operations and management.

```python
from src.vidgen.utils.file_manager import FileManager

file_manager = FileManager(config)
```

#### Methods

##### ensure_directory()

Ensure directory exists.

```python
def ensure_directory(self, path: str) -> str:
    """
    Ensure directory exists, create if necessary.
    
    Args:
        path: Directory path
    
    Returns:
        Absolute path to directory
    """
```

##### cleanup_temp_files()

Clean up temporary files.

```python
def cleanup_temp_files(self, older_than_hours: int = 24) -> int:
    """
    Clean up temporary files older than specified time.
    
    Args:
        older_than_hours: Age threshold in hours
    
    Returns:
        Number of files cleaned up
    """
```

### Logging and Progress Tracking

#### VidGenLogger Class

Enhanced logging with contextual information.

```python
from src.vidgen.utils.logging_config import VidGenLogger

logger = VidGenLogger("component_name")
```

#### ProgressTracker Class

Real-time progress tracking for long operations.

```python
from src.vidgen.utils.logging_config import ProgressTracker

tracker = ProgressTracker("operation_name", total_steps=100)
tracker.update(50, "Halfway complete")
```

## Usage Examples

### Basic Video Generation

```python
from src.vidgen.services.video_generator import VideoGenerator
from src.vidgen.core.config import Config

# Setup
config = Config()
generator = VideoGenerator(config)

# Generate video
script = """
A peaceful morning in the forest. Birds are singing in the trees.
The sun filters through the leaves, creating beautiful patterns on the ground.
A deer gracefully walks through the underbrush.
"""

video_path = generator.generate_video(
    script=script,
    output_path="outputs/forest_video.mp4",
    progress_callback=lambda p: print(f"Progress: {p}%")
)

print(f"Video generated: {video_path}")
```

### Advanced Audio Processing

```python
from src.vidgen.models.audio import AudioModel
from src.vidgen.core.config import Config

# Setup
config = Config()
audio_model = AudioModel(config)

# Generate multiple audio tracks
forest_ambient = audio_model.generate_audio(
    "peaceful forest ambient sounds with birds singing"
)

background_music = audio_model.generate_audio(
    "gentle acoustic guitar melody in G major"
)

# Mix the tracks
final_audio = audio_model.mix_audio(
    audio_paths=[forest_ambient, background_music],
    volumes=[0.7, 0.3]  # Ambient louder than music
)

print(f"Mixed audio: {final_audio}")
```

### Custom Video Effects

```python
from src.vidgen.models.video import VideoModel
from src.vidgen.core.config import Config

# Setup
config = Config()
video_model = VideoModel(config)

# Create video with transitions
images = ["scene1.jpg", "scene2.jpg", "scene3.jpg"]
audio = "narration.wav"

video_with_transitions = video_model.generate_video_with_transitions(
    image_paths=images,
    audio_path=audio,
    transition_type="slide_left",
    segment_duration=4.0
)

# Add motion effects
dynamic_video = video_model.add_motion_effects(
    video_path=video_with_transitions,
    effect_type="zoom_pan",
    intensity=0.3
)

print(f"Enhanced video: {dynamic_video}")
```

## Error Handling Examples

### Using Error Recovery

```python
from src.vidgen.core.exceptions import with_error_recovery, VidGenError

@with_error_recovery
def generate_content():
    # Your content generation code
    return video_generator.generate_video(script)

try:
    result = generate_content()
    print(f"Success: {result}")
except VidGenError as e:
    print(f"Error: {e}")
    print(f"Suggestion: {e.recovery_suggestion}")
    
    # Attempt recovery based on suggestion
    if "try reducing" in e.recovery_suggestion.lower():
        # Implement fallback strategy
        pass
```

### Manual Error Handling

```python
from src.vidgen.core.exceptions import ErrorRecovery, FFmpegError

try:
    video_path = video_model.generate_video_with_transitions(...)
except FFmpegError as e:
    recovery = ErrorRecovery()
    user_message = recovery.get_user_friendly_message(e)
    suggestion = recovery.get_recovery_suggestion(e)
    
    print(f"FFmpeg Error: {user_message}")
    print(f"Try: {suggestion}")
```
