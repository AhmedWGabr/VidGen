# VidGen API Reference 📚

This document provides comprehensive API documentation for VidGen's core modules, classes, and functions with detailed examples and usage patterns based on the actual implementation.

## 📑 Table of Contents

- [🔧 Core Configuration](#-core-configuration)
- [🚨 Error Handling](#-error-handling)
- [🎵 Audio Models](#-audio-models)
- [🖼️ Image Models](#%EF%B8%8F-image-models)
- [🗣️ Text-to-Speech](#%EF%B8%8F-text-to-speech)
- [🎬 Video Models](#-video-models)
- [⚙️ Services](#%EF%B8%8F-services)
- [🛠️ Utilities](#%EF%B8%8F-utilities)
- [💡 Usage Examples](#-usage-examples)
- [🔍 Error Handling Examples](#-error-handling-examples)

---

## 🔧 Core Configuration

### VideoGenConfig Class

The central configuration management system for VidGen with validation and directory management.

```python
from src.vidgen.core.config import VideoGenConfig

# Access configuration values
output_dir = VideoGenConfig.OUTPUT_DIR
model = VideoGenConfig.STABLE_DIFFUSION_MODEL

# Ensure directories exist
VideoGenConfig.ensure_dirs()

# Configure logging
VideoGenConfig.configure_logging()
```

#### 🔧 Configuration Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `STABLE_DIFFUSION_MODEL` | str | `"runwayml/stable-diffusion-v1-5"` | Stable Diffusion model identifier |
| `DEFAULT_SEGMENT_DURATION` | int | `5` | Default segment duration in seconds |
| `OUTPUT_DIR` | str | `"outputs"` | Directory for generated content |
| `TEMP_DIR` | str | `"temp"` | Temporary files directory |
| `GEMINI_MODEL` | str | `"gemini-2.0-flash-001"` | Google Gemini model version |
| `LOG_LEVEL` | int | `logging.INFO` | Logging verbosity level |

#### 🔧 Configuration Methods

##### `ensure_dirs() -> None`
```python
@classmethod
def ensure_dirs(cls):
    """Ensure output and temp directories exist."""
    os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
    os.makedirs(cls.TEMP_DIR, exist_ok=True)
```

##### `configure_logging() -> None`
```python
@classmethod
def configure_logging(cls):
    """Configure logging with standard format and level."""
    logging.basicConfig(
        level=cls.LOG_LEVEL,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
    )
```

#### Backward Compatibility

```python
# Config alias for backward compatibility
from src.vidgen.core.config import Config
# Config is an alias for VideoGenConfig
```

---

## 🚨 Error Handling

### Exception Classes

VidGen provides a comprehensive exception hierarchy for better error handling and debugging.

#### VidGenException

Base exception class for all VidGen errors.

```python
from src.vidgen.core.exceptions import VidGenException

class VidGenException(Exception):
    """Base exception for VidGen operations."""
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(message)
        self.original_exception = original_exception
```

#### Specialized Exceptions

```python
from src.vidgen.core.exceptions import (
    ScriptParsingError,
    ModelLoadError,
    AudioGenerationError,
    ImageGenerationError,
    VideoAssemblyError,
    ConfigurationError
)

# Example usage
try:
    generate_tts_audio(text)
except AudioGenerationError as e:
    print(f"TTS generation failed: {e}")
    # Implement fallback strategy
```

**Available Exception Types**:
- `ScriptParsingError` - Script analysis and parsing failures
- `ModelLoadError` - AI model loading and initialization errors
- `AudioGenerationError` - TTS and audio generation failures
- `ImageGenerationError` - Image generation and processing errors
- `VideoAssemblyError` - Video compilation and assembly failures
- `ConfigurationError` - Configuration validation errors

### Error Recovery Patterns

#### Try-Catch with Fallbacks

```python
from src.vidgen.core.exceptions import ImageGenerationError
from src.vidgen.models.image import generate_character_image

def safe_image_generation(prompt, seed=42):
    """Generate image with fallback handling."""
    try:
        return generate_character_image(prompt, seed)
    except ImageGenerationError as e:
        logging.warning(f"Image generation failed: {e}")
        return "placeholder_image.png"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None
```

#### Configuration Validation

```python
from src.vidgen.core.config import VideoGenConfig
from src.vidgen.core.exceptions import ConfigurationError

def validate_setup():
    """Validate VidGen setup and configuration."""
    try:
        VideoGenConfig.ensure_dirs()
        
        # Check required API keys
        if not os.getenv('GEMINI_API_KEY'):
            raise ConfigurationError("GEMINI_API_KEY environment variable required")
            
        return True
    except ConfigurationError as e:
        print(f"Configuration error: {e}")        return False
```

---

## 🎵 Audio Models

### Background Audio Generation

Advanced audio generation and processing capabilities using FFmpeg audio synthesis.

```python
from src.vidgen.models.audio import generate_background_audio, mix_audio

# Generate background audio
audio_path = generate_background_audio("peaceful forest ambient sounds")
```

#### generate_background_audio()

Generate background audio/music from audio command description.

```python
def generate_background_audio(audio_command: str) -> str:
    """
    Generate background audio/music from audio command description.
    Supports different audio types: ambient, music, and sound effects.
    
    Args:
        audio_command: Description of the background audio to generate
        
    Returns:
        Path to the generated audio file
        
    Examples:
        # Generate ambient sounds
        generate_background_audio("peaceful forest ambient sounds")
        
        # Generate music
        generate_background_audio("upbeat electronic music")
        
        # Generate silence
        generate_background_audio("silence")
    """
```

#### mix_audio()

Mix multiple audio tracks with volume control.

```python
def mix_audio(audio_paths: List[str], volumes: List[float] = None, 
              output_path: str = None) -> str:
    """
    Mix multiple audio tracks.
    
    Args:
        audio_paths: List of input audio file paths
        volumes: Volume levels (0.0-1.0) for each track
        output_path: Output file path (auto-generated if None)
    
    Returns:
        Path to mixed audio file
    """
```

#### Audio Processing Features

**Supported Audio Types**:
- **Silence**: Static or ambient silence
- **Ambient**: Nature sounds, room tones, atmospheric audio
- **Music**: Procedural music generation with FFmpeg
- **Sound Effects**: Short audio clips and effects

**Audio Formats**:
- Output: WAV format (44.1kHz, 16-bit)
- Processing: FFmpeg audio filters
- Duration: Auto-detected or specified

---

## 🖼️ Image Models

### Character Image Generation

AI-powered image generation using Stable Diffusion for character and scene creation.

```python
from src.vidgen.models.image import generate_character_image, get_image_pipeline

# Generate character image
image_path = generate_character_image("A young scientist with glasses", seed=42)

# Access the pipeline directly
pipeline = get_image_pipeline()
```

#### generate_character_image()

Generate a character image from text prompt with seed control.

```python
def generate_character_image(image_command, seed=42) -> str:
    """
    Generate a character image from the given prompt.
    
    Args:
        image_command: Image generation prompt (str) or command dictionary
        seed: Random seed for reproducible generation
        
    Returns:
        Path to the generated image file
        
    Examples:
        # Simple prompt
        generate_character_image("A wise old wizard", seed=123)
        
        # Command dictionary format
        generate_character_image({
            "face_prompt": "A young woman scientist",
            "character": "Dr. Sarah",
            "seed": 42
        })
    """
```

#### get_image_pipeline()

Get or initialize the Stable Diffusion pipeline with caching.

```python
def get_image_pipeline():
    """
    Get the cached Stable Diffusion pipeline or create if needed.
    
    Returns:
        StableDiffusionPipeline: Initialized and cached pipeline
        
    Features:
        - Thread-safe initialization
        - GPU acceleration when available
        - Model caching for performance
        - Error handling for missing dependencies
    """
```

#### Image Generation Features

**Model Support**:
- **Stable Diffusion**: Configurable model selection
- **GPU Acceleration**: CUDA support when available
- **CPU Fallback**: Automatic fallback for systems without GPU

**Output Features**:
- **Format**: PNG with transparency support
- **Resolution**: Configurable (default model resolution)
- **Seeding**: Reproducible generation with seeds
- **Caching**: Character face consistency across scenes

---

## 🗣️ Text-to-Speech

### TTS Audio Generation

High-quality text-to-speech using Bark TTS with voice synthesis capabilities.

```python
from src.vidgen.models.tts import generate_tts_audio

# Generate speech from text
audio_path = generate_tts_audio("Welcome to our AI video generation system.")
```

#### generate_tts_audio()

Convert text to speech using Bark TTS.

```python
def generate_tts_audio(tts_command: str) -> str:
    """
    Generate text-to-speech audio from the given text command.
    
    Args:
        tts_command: Text to convert to speech
        
    Returns:
        Path to the generated audio file (None if failed)
        
    Features:
        - High-quality Bark TTS integration
        - Unique filename generation
        - Audio directory management
        - Error handling with graceful fallbacks
        
    Examples:
        # Basic usage
        audio_path = generate_tts_audio("Hello, world!")
        
        # Longer text
        audio_path = generate_tts_audio('''
            Welcome to our presentation about artificial intelligence
            and machine learning in video generation.
        ''')
    """
```

#### TTS Features

**Audio Quality**:
- **Model**: Bark TTS with emotion synthesis
- **Format**: WAV format compatible with video assembly
- **Sample Rate**: Bark's native sample rate
- **Channels**: Mono audio optimized for speech

**Voice Features**:
- **Natural Speech**: Human-like intonation and pacing
- **Emotion**: Contextual emotion understanding
- **Consistency**: Stable voice characteristics across segments

**Error Handling**:
- **Dependency Checks**: Graceful handling when Bark is not available
- **Fallback**: Returns None for failed generation
- **Logging**: Detailed error logging for debugging

---

## 🎬 Video Models

### Video Processing and Effects

Video generation, effects, and post-processing functionality.

```python
from src.vidgen.models.video import (
    generate_video_segment,
    generate_video_with_transitions,
    add_motion_effects,
    create_multi_angle_video
)

# Generate basic video segment
video_path = generate_video_segment(video_command, face_cache={})
```

#### generate_video_segment()

Generate a single video segment from a command description.

```python
def generate_video_segment(video_command, face_cache=None, default_duration=5) -> str:
    """
    Generate a video segment from command description.
    
    Args:
        video_command: Video generation command (dict or str)
        face_cache: Character face consistency cache
        default_duration: Default segment duration in seconds
        
    Returns:
        Path to generated video segment
        
    Features:
        - Character image generation with caching
        - TTS audio generation
        - Video assembly with FFmpeg
        - Fallback handling for failed operations
    """
```

#### generate_video_with_transitions()

Create video with professional transitions between segments.

```python
def generate_video_with_transitions(segments, transition_type="fade", 
                                   transition_duration=0.5) -> str:
    """
    Generate video with transitions between segments.
    
    Args:
        segments: List of video segment paths
        transition_type: Type of transition effect
        transition_duration: Duration of transition in seconds
        
    Returns:
        Path to final video with transitions
        
    Transition Types:
        - "fade": Cross-fade between segments
        - "slide_left": Slide transition to left
        - "slide_right": Slide transition to right
        - "wipe": Wipe transition effect
    """
```

#### add_motion_effects()

Add motion effects to existing video.

```python
def add_motion_effects(video_path, effect_type="zoom_pan", intensity=0.1) -> str:
    """
    Add motion effects to video.
    
    Args:
        video_path: Input video file path
        effect_type: Effect type to apply
        intensity: Effect intensity (0.0-1.0)
        
    Returns:
        Path to processed video with effects
        
    Effect Types:
        - "zoom_pan": Ken Burns effect with zoom and pan
        - "parallax": Parallax motion effect
        - "shake": Camera shake effect
    """
```

#### create_multi_angle_video()

Create video with multiple camera angles and perspective changes.

```python
def create_multi_angle_video(image_path, audio_path, duration, angles=None) -> str:
    """
    Create multi-angle video effect from single image.
    
    Args:
        image_path: Source image file path
        audio_path: Audio track file path
        duration: Video duration in seconds
        angles: List of camera angles to apply
        
    Returns:
        Path to multi-angle video
        
    Angle Effects:
        - Dynamic cropping and scaling
        - Perspective transformations
        - Smooth angle transitions
    """
```

---

## ⚙️ Services

### Script Processing

Advanced script analysis and video assembly services.

```python
from src.vidgen.services.script_parser import parse_detailed_script
from src.vidgen.services.video_assembler import assemble_video
from src.vidgen.services.gemini_api import analyze_script_with_gemini

# Parse script into segments
segments = parse_detailed_script(script_text)

# Assemble final video
video_path = assemble_video(segments, output_path="final_video.mp4")
```

#### ScriptParser - parse_detailed_script()

Parse and segment script using Gemini API for intelligent analysis.

```python
def parse_detailed_script(script: str) -> dict:
    """
    Parse script into structured segments with Gemini AI analysis.
    
    Args:
        script: Raw script text
        
    Returns:
        Dictionary with parsed segments including:
        - tts: Text-to-speech segments
        - video: Video generation commands
        - audio: Background audio commands
        - characters: Identified characters
        
    Features:
        - Intelligent script segmentation
        - Character identification and consistency
        - Scene analysis and description
        - Timing and duration estimation
    """
```

#### VideoAssembler - assemble_video()

Assemble final video from generated components.

```python
def assemble_video(video_segments, tts_audios=None, background_audios=None, 
                  character_images=None, output_file="output.mp4") -> str:
    """
    Assemble final video from all generated components.
    
    Args:
        video_segments: List of video segment paths
        tts_audios: List of TTS audio paths
        background_audios: List of background audio paths
        character_images: List of character image paths
        output_file: Output video filename
        
    Returns:
        Path to assembled video file
        
    Features:
        - Multi-track audio mixing
        - Video concatenation with transitions
        - Audio synchronization
        - Quality optimization
    """
```

#### GeminiAPI - analyze_script_with_gemini()

Leverage Google Gemini for intelligent script analysis.

```python
def analyze_script_with_gemini(script: str, api_key: str) -> dict:
    """
    Analyze script using Google Gemini API.
    
    Args:
        script: Input script text
        api_key: Google Gemini API key
        
    Returns:
        Structured analysis including:
        - Scene breakdown
        - Character analysis
        - Narrative flow
        - Technical requirements
        
    Features:
        - Advanced natural language understanding
        - Context-aware segmentation
        - Character relationship mapping
        - Scene continuity analysis
    """
```

---

## 🛠️ Utilities

### File Management and Logging

Essential utility functions for file operations and system management.

```python
from src.vidgen.utils.file_manager import cleanup_temp_files, ensure_directory
from src.vidgen.utils.logging_config import setup_logging
from src.vidgen.utils.helpers import format_duration, validate_file_path

# File operations
ensure_directory("outputs/videos")
cleanup_temp_files(max_age_hours=24)

# Logging setup
setup_logging(level="INFO")
```

#### File Management

##### ensure_directory()

Ensure directory exists with proper permissions.

```python
def ensure_directory(path: str) -> str:
    """
    Ensure directory exists, create if necessary.
    
    Args:
        path: Directory path to create
        
    Returns:
        Absolute path to directory
        
    Features:
        - Recursive directory creation
        - Permission handling
        - Cross-platform compatibility
    """
```

##### cleanup_temp_files()

Clean up temporary files based on age and patterns.

```python
def cleanup_temp_files(older_than_hours: int = 24, 
                      pattern: str = "*") -> int:
    """
    Clean up temporary files older than specified time.
    
    Args:
        older_than_hours: Age threshold in hours
        pattern: File pattern to match
        
    Returns:
        Number of files cleaned up
        
    Features:
        - Age-based cleanup
        - Pattern matching
        - Safe deletion with logging
    """
```

#### Logging Configuration

##### setup_logging()

Configure comprehensive logging for VidGen operations.

```python
def setup_logging(level: str = "INFO", log_file: str = None) -> None:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
        
    Features:
        - Structured log formatting
        - Multiple output targets
        - Component-specific loggers
        - Performance tracking
    """
```

#### Helper Functions

##### format_duration()

Format duration values for display.

```python
def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "2m 30s")
    """
```

##### validate_file_path()

Validate file paths and extensions.

```python
def validate_file_path(path: str, expected_ext: str = None) -> bool:
    """
    Validate file path and optional extension.
    
    Args:
        path: File path to validate
        expected_ext: Expected file extension
        
    Returns:
        True if valid, False otherwise
    """
```

---

## 💡 Usage Examples

### Basic Video Generation Pipeline

```python
import os
from src.vidgen.core.config import VideoGenConfig
from src.vidgen.services.script_parser import parse_detailed_script
from src.vidgen.services.video_assembler import assemble_video

# Setup configuration
VideoGenConfig.ensure_dirs()
VideoGenConfig.configure_logging()

# Set API key
os.environ['GEMINI_API_KEY'] = 'your_api_key_here'

# Generate video from script
script = """
A peaceful morning in the forest. Birds are singing in the trees.
The sun filters through the leaves, creating beautiful patterns on the ground.
A deer gracefully walks through the underbrush.
"""

# Parse script using Gemini
parsed_content = parse_detailed_script(script)
print(f"Generated {len(parsed_content['video'])} video segments")

# Assemble final video
video_path = assemble_video(
    video_segments=parsed_content['video'],
    tts_audios=parsed_content['tts'],
    background_audios=parsed_content['audio'],
    output_file="forest_scene.mp4"
)

print(f"Video generated: {video_path}")
```

### Custom Audio Generation

```python
from src.vidgen.models.audio import generate_background_audio, mix_audio

# Generate different types of audio
forest_ambient = generate_background_audio(
    "peaceful forest ambient sounds with birds singing and wind"
)

soft_music = generate_background_audio(
    "gentle acoustic guitar background music in C major"
)

# Mix multiple audio tracks
final_audio = mix_audio(
    audio_paths=[forest_ambient, soft_music],
    volumes=[0.7, 0.3],  # Forest sounds louder than music
    output_path="outputs/audio/mixed_background.wav"
)

print(f"Mixed audio created: {final_audio}")
```

### Character-Consistent Image Generation

```python
from src.vidgen.models.image import generate_character_image

# Create character cache for consistency
face_cache = {}

# Generate character images with consistent appearance
characters = [
    {"name": "Dr. Sarah", "prompt": "A young woman scientist with glasses and lab coat"},
    {"name": "Professor Kim", "prompt": "An elderly professor with gray beard and tweed jacket"}
]

for character in characters:
    image_path = generate_character_image(
        {
            "character": character["name"],
            "face_prompt": character["prompt"],
            "seed": hash(character["name"]) % 10000  # Consistent seed per character
        }
    )
    face_cache[character["name"]] = image_path
    print(f"Generated {character['name']}: {image_path}")
```

### Advanced Video Effects

```python
from src.vidgen.models.video import (
    generate_video_segment,
    generate_video_with_transitions,
    add_motion_effects
)

# Generate individual video segments
segments = []
scene_descriptions = [
    "A laboratory with scientific equipment and computers",
    "A conference room with presentation screen",
    "An outdoor research facility with solar panels"
]

for i, scene in enumerate(scene_descriptions):
    video_command = {
        "start": i * 5,
        "end": (i + 1) * 5,
        "scene": scene,
        "narration": f"Scene {i+1} narration text here"
    }
    
    segment_path = generate_video_segment(video_command, face_cache={})
    segments.append(segment_path)

# Add transitions between segments
video_with_transitions = generate_video_with_transitions(
    segments=segments,
    transition_type="fade",
    transition_duration=0.8
)

# Add motion effects
final_video = add_motion_effects(
    video_path=video_with_transitions,
    effect_type="zoom_pan",
    intensity=0.2
)

print(f"Final video with effects: {final_video}")
```

---

## 🔍 Error Handling Examples

### Comprehensive Error Handling

```python
import logging
from src.vidgen.core.exceptions import (
    VidGenException, 
    ScriptParsingError, 
    ModelLoadError,
    AudioGenerationError,
    ImageGenerationError
)
from src.vidgen.models.tts import generate_tts_audio
from src.vidgen.models.image import generate_character_image
from src.vidgen.services.script_parser import parse_detailed_script

def safe_video_generation(script_text):
    """Example of comprehensive error handling in video generation."""
    
    try:
        # Parse script with error handling
        try:
            parsed_content = parse_detailed_script(script_text)
        except ScriptParsingError as e:
            logging.error(f"Script parsing failed: {e}")
            # Use fallback parsing or manual segmentation
            parsed_content = {"tts": [script_text], "video": [], "audio": []}
        
        # Generate TTS with fallback
        audio_files = []
        for tts_text in parsed_content["tts"]:
            try:
                audio_path = generate_tts_audio(tts_text)
                if audio_path:
                    audio_files.append(audio_path)
            except AudioGenerationError as e:
                logging.warning(f"TTS generation failed for '{tts_text[:30]}...': {e}")
                # Continue with other audio segments
                continue
        
        # Generate images with error recovery
        image_files = []
        for video_cmd in parsed_content["video"]:
            try:
                image_path = generate_character_image(
                    video_cmd.get("scene", "A neutral background"),
                    seed=42
                )
                image_files.append(image_path)
            except ImageGenerationError as e:
                logging.warning(f"Image generation failed: {e}")
                # Use placeholder image
                image_files.append("placeholder_image.png")
            except ModelLoadError as e:
                logging.error(f"Model loading failed: {e}")
                # Could implement CPU fallback or exit gracefully
                break
        
        return {
            "audio_files": audio_files,
            "image_files": image_files,
            "success": True
        }
        
    except VidGenException as e:
        logging.error(f"VidGen operation failed: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"success": False, "error": f"Unexpected error: {e}"}

# Usage with error handling
result = safe_video_generation("Your script text here")
if result["success"]:
    print(f"Generated {len(result['audio_files'])} audio files")
    print(f"Generated {len(result['image_files'])} image files")
else:
    print(f"Generation failed: {result['error']}")
```

### Configuration and Setup Validation

```python
import os
import logging
from src.vidgen.core.config import VideoGenConfig
from src.vidgen.core.exceptions import ConfigurationError

def validate_vidgen_setup():
    """Validate complete VidGen setup before generation."""
    
    validation_results = {
        "directories": False,
        "api_keys": False,
        "dependencies": False,
        "models": False
    }
    
    # Check directories
    try:
        VideoGenConfig.ensure_dirs()
        validation_results["directories"] = True
        logging.info("✓ Directories validated")
    except Exception as e:
        logging.error(f"✗ Directory setup failed: {e}")
    
    # Check API keys
    try:
        if not os.getenv('GEMINI_API_KEY'):
            raise ConfigurationError("GEMINI_API_KEY not set")
        validation_results["api_keys"] = True
        logging.info("✓ API keys validated")
    except ConfigurationError as e:
        logging.error(f"✗ API configuration failed: {e}")
    
    # Check dependencies
    try:
        import torch
        import diffusers
        from bark import generate_audio
        validation_results["dependencies"] = True
        logging.info("✓ Dependencies validated")
    except ImportError as e:
        logging.error(f"✗ Missing dependency: {e}")
    
    # Check model access
    try:
        from src.vidgen.models.image import get_image_pipeline
        pipeline = get_image_pipeline()
        validation_results["models"] = True
        logging.info("✓ Models validated")
    except Exception as e:
        logging.error(f"✗ Model loading failed: {e}")
    
    # Summary
    all_valid = all(validation_results.values())
    if all_valid:
        logging.info("🎉 VidGen setup validation successful!")
    else:
        failed_checks = [k for k, v in validation_results.items() if not v]
        logging.error(f"❌ Setup validation failed: {failed_checks}")
    
    return validation_results

# Run validation before starting
if __name__ == "__main__":
    VideoGenConfig.configure_logging()
    validation = validate_vidgen_setup()
    
    if all(validation.values()):
        print("Ready to generate videos!")
    else:
        print("Please fix setup issues before proceeding.")
```

---

*For more detailed information about installation, configuration, and advanced usage, see:*
- [Setup Guide](setup.md) - Installation and configuration instructions
- [Examples](examples.md) - Additional usage examples and tutorials
- [Migration Guide](MIGRATION_GUIDE.md) - Upgrading from legacy versions
- [Model Files](../MODEL_FILES.md) - AI model documentation and optimization

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
