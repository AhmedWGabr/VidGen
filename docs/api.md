# VidGen API Reference

This document provides comprehensive API documentation for the VidGen video generation framework, covering all modules, classes, and functions with practical examples.

## Table of Contents
1. [Package Overview](#package-overview)
2. [Core Components](#core-components)
3. [Model Interfaces](#model-interfaces)
4. [Service Components](#service-components)
5. [User Interface](#user-interface)
6. [Utilities](#utilities)
7. [Error Handling](#error-handling)
8. [Usage Examples](#usage-examples)

## Package Overview

VidGen is organized into a modular architecture with clear separation of concerns:

```
vidgen/
├── core/           # Core configuration and foundational components
├── models/         # AI model interfaces and implementations
├── services/       # Business logic and processing services
├── ui/             # User interface components (Gradio, CLI)
├── utils/          # Utility functions and helpers
└── exceptions/     # Custom exception classes
```

### Quick Start
```python
from vidgen import VidGen
from vidgen.core.config import VideoGenConfig

# Initialize with API key
vg = VidGen(api_key="your_gemini_api_key")

# Generate a video
result = vg.generate_video(
    script="A beautiful sunset over mountains.",
    output_filename="sunset.mp4"
)
```

## Core Components

### Configuration (`vidgen.core.config`)

Central configuration management system for the entire VidGen framework.

#### `VideoGenConfig` Class

The main configuration class that manages all settings and provides environment-based configuration.

```python
from vidgen.core.config import VideoGenConfig

class VideoGenConfig:
    # Core Settings
    OUTPUT_DIR: str = "./outputs"
    TEMP_DIR: str = "./outputs/temp"
    LOG_LEVEL: str = "INFO"
    DEVICE: str = "auto"  # auto, cpu, cuda, mps
    
    # Model Settings
    STABLE_DIFFUSION_MODEL: str = "runwayml/stable-diffusion-v1-5"
    TTS_MODEL: str = "bark"
    BARK_MODEL_SIZE: str = "small"
    
    # Video Settings
    DEFAULT_SEGMENT_DURATION: int = 5
    MAX_SEGMENTS: int = 20
    VIDEO_FPS: int = 30
    VIDEO_RESOLUTION: str = "1920x1080"
    
    # Performance Settings
    HALF_PRECISION: bool = False
    USE_STREAMING: bool = False
    AUTO_CLEANUP: bool = True
    
    @classmethod
    def load_from_file(cls, config_path: str) -> None:
        """Load configuration from YAML or JSON file"""
        
    @classmethod
    def save_to_file(cls, config_path: str) -> None:
        """Save current configuration to file"""
        
    @classmethod
    def get_device(cls) -> str:
        """Get optimal device for computation"""
        
    @classmethod
    def validate_config(cls) -> bool:
        """Validate current configuration settings"""
```

**Usage Examples:**
```python
# Basic configuration
VideoGenConfig.OUTPUT_DIR = "/custom/output/path"
VideoGenConfig.STABLE_DIFFUSION_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

# Environment-specific optimization
if VideoGenConfig.get_device() == "cuda":
    VideoGenConfig.HALF_PRECISION = True
    VideoGenConfig.VIDEO_RESOLUTION = "3840x2160"  # 4K for powerful GPUs

# Load configuration from file
VideoGenConfig.load_from_file("production_config.yaml")

# Validate settings
if not VideoGenConfig.validate_config():
    raise ValueError("Invalid configuration detected")
```

## Model Interfaces

### Audio Generation (`vidgen.models.audio`)

Handles background audio and music generation for videos.

#### `AudioModel` Class

```python
from vidgen.models.audio import AudioModel
from vidgen.core.config import VideoGenConfig

class AudioModel:
    def __init__(self, config: VideoGenConfig):
        """Initialize audio generation model"""
        
    def generate_audio(self, 
                      description: str,
                      duration: float = 30.0,
                      style: str = "ambient",
                      seed: Optional[int] = None) -> str:
        """
        Generate background audio based on description.
        
        Args:
            description: Text description of desired audio
            duration: Audio length in seconds
            style: Audio style (ambient, upbeat, dramatic, etc.)
            seed: Random seed for reproducibility
            
        Returns:
            Path to generated audio file
            
        Example:
            audio_path = audio_model.generate_audio(
                "Peaceful forest sounds with birds chirping",
                duration=60,
                style="natural"
            )
        """
        
    def generate_background_music(self,
                                genre: str = "ambient",
                                mood: str = "calm",
                                duration: float = 30.0,
                                instruments: List[str] = None) -> str:
        """Generate background music with specific parameters"""
        
    def adjust_audio_levels(self, 
                           audio_path: str,
                           target_volume: float = 0.3,
                           fade_in: float = 1.0,
                           fade_out: float = 1.0) -> str:
        """Adjust audio levels and apply fading effects"""
```

**Usage Examples:**
```python
from vidgen.models.audio import AudioModel
from vidgen.core.config import VideoGenConfig

audio_model = AudioModel(VideoGenConfig())

# Generate ambient background music
bg_music = audio_model.generate_audio(
    description="Soft piano melody for meditation",
    duration=120,
    style="peaceful"
)

# Generate nature sounds
nature_audio = audio_model.generate_background_music(
    genre="nature",
    mood="serene",
    duration=60,
    instruments=["birds", "water", "wind"]
)
```

### Image Generation (`vidgen.models.image`)

Manages image and character generation using Stable Diffusion models.

#### `ImageModel` Class

```python
from vidgen.models.image import ImageModel
from vidgen.core.config import VideoGenConfig

class ImageModel:
    def __init__(self, config: VideoGenConfig):
        """Initialize image generation model"""
        
    def generate_image(self,
                      prompt: str,
                      negative_prompt: str = "",
                      width: int = 1024,
                      height: int = 1024,
                      guidance_scale: float = 7.5,
                      num_inference_steps: int = 50,
                      seed: Optional[int] = None) -> str:
        """
        Generate a single image from text prompt.
        
        Args:
            prompt: Detailed description of desired image
            negative_prompt: What to avoid in the image
            width: Image width in pixels
            height: Image height in pixels
            guidance_scale: How closely to follow the prompt (1-20)
            num_inference_steps: Quality vs speed tradeoff (10-100)
            seed: Random seed for reproducibility
            
        Returns:
            Path to generated image file
        """
        
    def generate_character_image(self,
                               character_description: str,
                               pose: str = "neutral",
                               background: str = "simple",
                               art_style: str = "realistic",
                               seed: Optional[int] = None) -> str:
        """Generate consistent character images"""
        
    def generate_scene_image(self,
                           scene_description: str,
                           lighting: str = "natural",
                           composition: str = "balanced",
                           camera_angle: str = "medium",
                           seed: Optional[int] = None) -> str:
        """Generate scene/environment images"""
        
    def upscale_image(self, 
                     image_path: str,
                     scale_factor: int = 2,
                     method: str = "esrgan") -> str:
        """Upscale images for higher resolution"""
```

**Usage Examples:**
```python
from vidgen.models.image import ImageModel

image_model = ImageModel(VideoGenConfig())

# Generate a landscape scene
landscape = image_model.generate_scene_image(
    scene_description="Majestic mountain range at golden hour",
    lighting="golden_hour",
    composition="wide_angle",
    camera_angle="low"
)

# Generate a character with consistency
character = image_model.generate_character_image(
    character_description="Friendly robot with blue LED eyes",
    pose="standing_confident",
    background="tech_lab",
    art_style="sci_fi"
)

# High-quality detailed image
detailed_image = image_model.generate_image(
    prompt="Cyberpunk cityscape at night, neon lights, rain",
    negative_prompt="blurry, low quality, distorted",
    width=1920,
    height=1080,
    guidance_scale=8.0,
    num_inference_steps=75
)
```

### Text-to-Speech (`vidgen.models.tts`)

Handles voice generation and speech synthesis using Bark TTS.

#### `TTSModel` Class

```python
from vidgen.models.tts import TTSModel

class TTSModel:
    def __init__(self, config: VideoGenConfig):
        """Initialize TTS model"""
        
    def generate_speech(self,
                       text: str,
                       voice: str = "default",
                       emotion: str = "neutral",
                       speed: float = 1.0,
                       pitch: float = 1.0) -> str:
        """
        Convert text to natural speech.
        
        Args:
            text: Text to convert to speech
            voice: Voice identifier (male_1, female_1, etc.)
            emotion: Emotional tone (neutral, happy, sad, excited)
            speed: Speech rate multiplier (0.5-2.0)
            pitch: Pitch adjustment (-1.0 to 1.0)
            
        Returns:
            Path to generated audio file
        """
        
    def list_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available voice options"""
        
    def clone_voice(self, 
                   reference_audio: str,
                   target_text: str) -> str:
        """Clone voice from reference audio (if supported)"""
        
    def add_speech_effects(self,
                          audio_path: str,
                          effects: List[str]) -> str:
        """Apply effects like reverb, echo, etc."""
```

**Usage Examples:**
```python
from vidgen.models.tts import TTSModel

tts_model = TTSModel(VideoGenConfig())

# Generate natural narration
narration = tts_model.generate_speech(
    text="Welcome to our exploration of quantum physics.",
    voice="narrator_male",
    emotion="confident",
    speed=0.9
)

# Get available voices
voices = tts_model.list_available_voices()
print(f"Available voices: {[v['name'] for v in voices]}")

# Generate with different emotions
excited_speech = tts_model.generate_speech(
    text="This is absolutely incredible!",
    voice="female_1",
    emotion="excited",
    speed=1.1
)
```

### Video Processing (`vidgen.models.video`)

Handles video segment generation and processing operations.

#### `VideoModel` Class

```python
from vidgen.models.video import VideoModel

class VideoModel:
    def __init__(self, config: VideoGenConfig):
        """Initialize video processing model"""
        
    def generate_video_segment(self,
                             image_paths: List[str],
                             audio_path: str = None,
                             duration: float = 5.0,
                             transition_in: str = "fade",
                             transition_out: str = "fade",
                             effects: List[str] = None) -> str:
        """
        Create a video segment from images and audio.
        
        Args:
            image_paths: List of image file paths
            audio_path: Background audio file
            duration: Segment duration in seconds
            transition_in: Entrance transition effect
            transition_out: Exit transition effect
            effects: List of video effects to apply
            
        Returns:
            Path to generated video segment
        """
        
    def apply_video_effects(self,
                           video_path: str,
                           effects: List[Dict]) -> str:
        """Apply visual effects to video"""
        
    def stabilize_video(self, video_path: str) -> str:
        """Apply video stabilization"""
        
    def color_correct(self,
                     video_path: str,
                     brightness: float = 1.0,
                     contrast: float = 1.0,
                     saturation: float = 1.0) -> str:
        """Apply color correction"""
        
    def add_motion_effects(self,
                          image_path: str,
                          motion_type: str,
                          duration: float = 5.0) -> str:
        """Add motion to static images (ken burns, parallax, etc.)"""
```

**Usage Examples:**
```python
from vidgen.models.video import VideoModel

video_model = VideoModel(VideoGenConfig())

# Create a video segment with effects
segment = video_model.generate_video_segment(
    image_paths=["scene1.jpg", "scene2.jpg"],
    audio_path="background.mp3",
    duration=8.0,
    transition_in="slide_right",
    transition_out="fade",
    effects=["color_grade", "stabilization"]
)

# Add motion to static image
motion_video = video_model.add_motion_effects(
    image_path="landscape.jpg",
    motion_type="ken_burns",
    duration=6.0
)

# Apply color correction
corrected = video_model.color_correct(
    video_path="raw_video.mp4",
    brightness=1.1,
    contrast=1.2,
    saturation=0.9
)
```

# Apply post-processing effects 
enhanced_video = apply_effects(
    video_path=output_path,
    effects=["color_grading", "stabilization"]
)
```

## Model Components

### Data Models (`vidgen.models.data_models`)

Pydantic models for validation and structured data representation.

```python
from vidgen.models.data_models import Character, ScriptSegment, VideoProject

# Create a character
character = Character(
    name="Sarah",
    description="A young scientist with glasses and a lab coat",
    seed=42  # Consistent seed for reproducible generation
)

# Create a script segment
segment = ScriptSegment(
    timestamp=0.0,
    duration=5.0,
    narration="Our journey begins in a state-of-the-art laboratory.",
    character=character,
    scene_description="Modern laboratory with glowing equipment"
)

# Create a complete project
project = VideoProject(
    script="A documentary about scientific discovery",
    segments=[segment],
    characters=[character],
    output_path="/path/to/output.mp4"
)
```

### Text-to-Speech (`vidgen.models.tts`)

Generates audio narration from text using ML-based text-to-speech models.

```python
from vidgen.models.tts import generate_tts_audio

# Generate audio from text
audio_path = generate_tts_audio("Welcome to our video about machine learning.")

# Generate with specific voice settings (if supported by model)
custom_audio = generate_tts_audio(
    text="Welcome to our video about machine learning.",
    voice="female_1",
    speed=1.2
)
```

### Image Generation (`vidgen.models.image`)

Creates character images and scene backgrounds using Stable Diffusion.

```python
from vidgen.models.image import generate_character_image, get_image_pipeline

# Generate a character image with consistent seed for reproducibility
image_path = generate_character_image(
    "A young woman scientist with glasses and a lab coat",
    seed=42
)

# For more complex usage, access the pipeline directly
pipeline = get_image_pipeline()
```

### Video Generation (`vidgen.models.video`)

Creates video segments from parsed script segments.

```python
from vidgen.models.video import generate_video_segment

# Create a face cache for consistent character appearance
face_cache = {}

# Generate a video segment from a parsed command
video_path = generate_video_segment(
    {
        "start": 0,
        "end": 5,
        "scene": "A laboratory with scientific equipment",
        "narration": "Our journey begins in a state-of-the-art laboratory."
    },
    face_cache=face_cache
)
```

### Audio Processing (`vidgen.models.audio`)

Handle background music and sound effects.

```python
from vidgen.models.audio import generate_background_audio, mix_audio

# Generate ambient background sound
bg_path = generate_background_audio("laboratory ambience with quiet beeping")

# Mix audio tracks with appropriate levels
mixed_audio = mix_audio(
    tracks=[voice_track, bg_track], 
    levels=[1.0, 0.3]  # Lower volume for background
)
```

## Service Components

### Script Parsing (`vidgen.services.script_parser`)

Handles conversion of user scripts and API responses into structured data for video generation.

#### `ScriptParser` Class

```python
from vidgen.services.script_parser import ScriptParser

class ScriptParser:
    def __init__(self):
        """Initialize script parser"""
        
    def parse_user_script(self, script: str) -> Dict[str, Any]:
        """
        Parse user-provided script into structured format.
        
        Args:
            script: Raw script text with visual descriptions and dialogue
            
        Returns:
            Structured data with video, audio, and TTS components
            
        Example:
            parser = ScriptParser()
            parsed = parser.parse_user_script('''
                A sunrise over mountains.
                [Background: Peaceful music]
                
                NARRATOR: "Good morning, world."
            ''')
        """
        
    def parse_detailed_script(self, json_data: str) -> Dict[str, List]:
        """Parse detailed script JSON from Gemini API"""
        
    def validate_script_segment(self, segment: Dict) -> bool:
        """Validate individual script segment"""
        
    def extract_characters(self, script: str) -> List[Dict]:
        """Extract character information from script"""
        
    def estimate_duration(self, parsed_script: Dict) -> float:
        """Estimate total video duration from parsed script"""
```

**Usage Examples:**
```python
from vidgen.services.script_parser import ScriptParser

parser = ScriptParser()

# Parse a user script
script = """
Title: "Nature Documentary"

A majestic eagle soars over a vast canyon.
[Background: Epic orchestral music]

NARRATOR (David): "In the wild, survival depends on adaptation."

Close-up of the eagle's piercing eyes.

NARRATOR (David): "Every decision can mean the difference between life and death."
"""

parsed = parser.parse_user_script(script)
print(f"Video segments: {len(parsed['video'])}")
print(f"Audio cues: {len(parsed['audio'])}")
print(f"Narration: {len(parsed['tts'])}")

# Estimate duration
duration = parser.estimate_duration(parsed)
print(f"Estimated duration: {duration} seconds")
```

### Gemini API Integration (`vidgen.services.gemini_api`)

Manages communication with Google's Gemini API for script enhancement and generation.

#### `GeminiAPIService` Class

```python
from vidgen.services.gemini_api import GeminiAPIService

class GeminiAPIService:
    def __init__(self, api_key: str):
        """Initialize Gemini API service"""
        
    def generate_detailed_script(self,
                               user_script: str,
                               segment_duration: int = 5,
                               target_length: int = 30) -> str:
        """
        Convert basic script to detailed JSON format.
        
        Args:
            user_script: Basic script from user
            segment_duration: Desired length of each segment
            target_length: Target total video length
            
        Returns:
            Detailed JSON script with timestamps and commands
        """
        
    def enhance_script(self, 
                      basic_script: str,
                      style: str = "documentary",
                      audience: str = "general") -> str:
        """Enhance script with additional details and improvements"""
        
    def generate_script_from_topic(self,
                                  topic: str,
                                  duration: int = 60,
                                  style: str = "educational") -> str:
        """Generate complete script from topic description"""
        
    def suggest_improvements(self, script: str) -> List[str]:
        """Get suggestions for script improvements"""
```

**Usage Examples:**
```python
from vidgen.services.gemini_api import GeminiAPIService

gemini = GeminiAPIService(api_key="your_api_key")

# Generate script from topic
script = gemini.generate_script_from_topic(
    topic="The benefits of renewable energy",
    duration=120,
    style="educational"
)

# Enhance existing script
enhanced = gemini.enhance_script(
    basic_script="Solar panels convert sunlight to electricity.",
    style="documentary",
    audience="adults"
)

# Get improvement suggestions
suggestions = gemini.suggest_improvements(script)
for suggestion in suggestions:
    print(f"💡 {suggestion}")
```

### Video Assembly (`vidgen.services.video_assembler`)

Combines all generated assets into final video with professional effects and transitions.

#### `VideoAssembler` Class

```python
from vidgen.services.video_assembler import VideoAssembler

class VideoAssembler:
    def __init__(self, config: VideoGenConfig):
        """Initialize video assembler"""
        
    def assemble_video(self,
                      video_segments: List[str],
                      tts_audios: List[str],
                      background_audios: List[str] = None,
                      output_file: str = "output.mp4",
                      transitions: List[str] = None) -> str:
        """
        Assemble final video from all components.
        
        Args:
            video_segments: List of video segment file paths
            tts_audios: List of TTS audio file paths
            background_audios: List of background audio files
            output_file: Output video file path
            transitions: List of transition effects between segments
            
        Returns:
            Path to assembled video file
        """
        
    def add_intro_outro(self,
                       video_path: str,
                       intro_template: str = None,
                       outro_template: str = None) -> str:
        """Add intro and outro sequences"""
        
    def apply_transitions(self,
                         video_segments: List[str],
                         transition_types: List[str]) -> List[str]:
        """Apply transitions between video segments"""
        
    def mix_audio_tracks(self,
                        narration: List[str],
                        background: List[str],
                        narration_volume: float = 0.8,
                        background_volume: float = 0.3) -> str:
        """Mix multiple audio tracks with proper levels"""
        
    def add_captions(self,
                    video_path: str,
                    subtitle_file: str = None,
                    auto_generate: bool = True) -> str:
        """Add captions/subtitles to video"""
```

**Usage Examples:**
```python
from vidgen.services.video_assembler import VideoAssembler

assembler = VideoAssembler(VideoGenConfig())

# Assemble complete video
final_video = assembler.assemble_video(
    video_segments=["seg1.mp4", "seg2.mp4", "seg3.mp4"],
    tts_audios=["narration1.wav", "narration2.wav"],
    background_audios=["bg_music.mp3"],
    transitions=["fade", "slide_left", "dissolve"],
    output_file="final_production.mp4"
)

# Add professional intro/outro
branded_video = assembler.add_intro_outro(
    video_path=final_video,
    intro_template="templates/company_intro.mp4",
    outro_template="templates/subscribe_outro.mp4"
)

# Add captions for accessibility
captioned_video = assembler.add_captions(
    video_path=branded_video,
    auto_generate=True
)
```

## User Interface

### Gradio Web Interface (`vidgen.ui.gradio_app`)

Provides an intuitive web-based interface for video generation.

#### `GradioInterface` Class

```python
from vidgen.ui.gradio_app import GradioInterface

class GradioInterface:
    def __init__(self, vidgen_app):
        """Initialize Gradio interface"""
        
    def launch(self,
              port: int = 7860,
              share: bool = False,
              debug: bool = False,
              auth: Tuple[str, str] = None) -> None:
        """
        Launch the web interface.
        
        Args:
            port: Port number for the web server
            share: Create public link (gradio.live)
            debug: Enable debug mode
            auth: Username/password tuple for authentication
        """
        
    def create_interface(self) -> gr.Interface:
        """Create and configure the Gradio interface"""
        
    def generate_video_ui(self,
                         script: str,
                         api_key: str,
                         duration: int,
                         quality: str) -> Tuple[str, str]:
        """UI callback for video generation"""
```

### Command Line Interface (`vidgen.ui.cli`)

Command-line interface for batch processing and automation.

#### CLI Commands

```bash
# Basic video generation
python -m vidgen.cli generate --script path/to/script.txt --output video.mp4

# Batch processing
python -m vidgen.cli batch --input-dir scripts/ --output-dir videos/

# Configuration management
python -m vidgen.cli config --set OUTPUT_DIR=/custom/path
python -m vidgen.cli config --show

# Model management
python -m vidgen.cli models --download all
python -m vidgen.cli models --list
python -m vidgen.cli models --clear-cache
```

## Utilities

### Progress Tracking (`vidgen.utils.progress`)

Provides real-time progress monitoring for long-running operations.

#### `ProgressTracker` Class

```python
from vidgen.utils.progress import ProgressTracker

class ProgressTracker:
    def __init__(self, task_name: str, total_steps: int):
        """Initialize progress tracker"""
        
    def update(self, 
               current_step: int,
               message: str = "",
               detailed_info: Dict = None) -> None:
        """Update progress with current step and message"""
        
    def set_substep(self, 
                   substep: int,
                   total_substeps: int,
                   message: str = "") -> None:
        """Update progress for substeps within a main step"""
        
    def complete(self, final_message: str = "Complete") -> None:
        """Mark task as completed"""
        
    def error(self, error_message: str) -> None:
        """Report error state"""
```

**Usage Examples:**
```python
from vidgen.utils.progress import ProgressTracker

# Basic progress tracking
tracker = ProgressTracker("Video Generation", total_steps=5)

tracker.update(1, "Parsing script...")
# ... processing ...

tracker.update(2, "Generating images...")
for i in range(10):
    tracker.set_substep(i+1, 10, f"Generating image {i+1}")
    # ... generate image ...

tracker.update(3, "Creating audio...")
tracker.update(4, "Assembling video...")
tracker.update(5, "Applying final effects...")
tracker.complete("Video generation successful!")
```

### File Management (`vidgen.utils.file_manager`)

Handles file operations, cleanup, and organization.

#### `FileManager` Class

```python
from vidgen.utils.file_manager import FileManager

class FileManager:
    def __init__(self, base_dir: str = None):
        """Initialize file manager"""
        
    def create_project_structure(self, project_name: str) -> str:
        """Create organized directory structure for a project"""
        
    def cleanup_temp_files(self, 
                          max_age_hours: int = 24,
                          preserve_cache: bool = True) -> None:
        """Clean up temporary files older than specified age"""
        
    def organize_assets(self, 
                       video_path: str,
                       keep_intermediates: bool = False) -> Dict[str, List[str]]:
        """Organize generated assets into proper directories"""
        
    def backup_project(self, 
                      project_dir: str,
                      backup_location: str = None) -> str:
        """Create backup of project directory"""
        
    def get_disk_usage(self) -> Dict[str, float]:
        """Get disk usage statistics for VidGen directories"""
```

### Logging Configuration (`vidgen.utils.logging_config`)

Configures comprehensive logging for debugging and monitoring.

#### Functions

```python
from vidgen.utils.logging_config import setup_logging, get_logger

def setup_logging(level: str = "INFO",
                 log_file: str = None,
                 enable_console: bool = True,
                 enable_progress: bool = True) -> None:
    """Configure logging for VidGen"""

def get_logger(name: str) -> logging.Logger:
    """Get configured logger instance"""

# Usage
setup_logging(level="DEBUG", log_file="vidgen.log")
logger = get_logger(__name__)

logger.info("Starting video generation")
logger.debug("Using model: stable-diffusion-v1-5")
logger.warning("GPU memory is low")
logger.error("Failed to generate image")
```

## Error Handling

### Exception Hierarchy (`vidgen.core.exceptions`)

Comprehensive exception system for specific error handling.

```python
from vidgen.core.exceptions import (
    VidGenError,           # Base exception
    ConfigurationError,    # Configuration issues
    ModelLoadError,        # Model loading failures
    ScriptParsingError,    # Script parsing problems
    AudioGenerationError,  # Audio generation issues
    ImageGenerationError,  # Image generation issues
    VideoAssemblyError,    # Video assembly problems
    APIError              # External API errors
)

# Error recovery decorator
from vidgen.core.exceptions import with_error_recovery

@with_error_recovery
def risky_operation():
    # Code that might fail
    pass

# Try operation with automatic recovery
try:
    result = risky_operation()
except VidGenError as e:
    print(f"Error: {e}")
    print(f"Suggestion: {e.recovery_suggestion}")
    print(f"Error code: {e.error_code}")
```

## Usage Examples

### Complete Video Generation Workflow

```python
from vidgen import VidGen
from vidgen.core.config import VideoGenConfig
from vidgen.utils.progress import ProgressTracker
from vidgen.core.exceptions import VidGenError

# Configure VidGen
VideoGenConfig.OUTPUT_DIR = "./my_videos"
VideoGenConfig.STABLE_DIFFUSION_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
VideoGenConfig.VIDEO_RESOLUTION = "1920x1080"
VideoGenConfig.HALF_PRECISION = True

# Initialize VidGen
vg = VidGen(api_key="your_gemini_api_key")

# Define script
script = """
Title: "The Future of Space Exploration"

A stunning view of Earth from space, with the International Space Station visible.
[Background: Inspiring orchestral music]

NARRATOR: "Humanity's greatest adventure is just beginning."

Animation of a Mars colony with domed structures and rovers.

NARRATOR: "Within the next two decades, humans will call Mars home."

Futuristic spacecraft traveling between planets.

NARRATOR: "The cosmos awaits our exploration."
"""

try:
    # Generate video with progress tracking
    result = vg.generate_video(
        script=script,
        segment_duration=6,
        output_filename="space_exploration.mp4",
        quality_preset="high",
        include_captions=True
    )
    
    print(f"✅ Video generated successfully!")
    print(f"📁 Location: {result.video_path}")
    print(f"⏱️ Duration: {result.metadata['duration']} seconds")
    print(f"📊 File size: {result.metadata['file_size_mb']:.1f} MB")
    print(f"🎨 Assets created: {len(result.image_paths)} images, {len(result.audio_paths)} audio files")
    
except VidGenError as e:
    print(f"❌ Generation failed: {e}")
    print(f"💡 Suggestion: {e.recovery_suggestion}")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

### Advanced Custom Pipeline

```python
from vidgen.models import AudioModel, ImageModel, TTSModel, VideoModel
from vidgen.services import ScriptParser, VideoAssembler
from vidgen.core.config import VideoGenConfig

# Initialize components
config = VideoGenConfig()
parser = ScriptParser()
audio_model = AudioModel(config)
image_model = ImageModel(config)
tts_model = TTSModel(config)
video_model = VideoModel(config)
assembler = VideoAssembler(config)

# Parse script
parsed_script = parser.parse_user_script(script)

# Generate assets in parallel
import asyncio

async def generate_assets():
    # Generate images
    image_tasks = [
        image_model.generate_scene_image(cmd['description'])
        for cmd in parsed_script['video']
    ]
    
    # Generate audio
    audio_tasks = [
        audio_model.generate_audio(cmd['description'])
        for cmd in parsed_script['audio']
    ]
    
    # Generate TTS
    tts_tasks = [
        tts_model.generate_speech(cmd['text'])
        for cmd in parsed_script['tts']
    ]
    
    # Wait for all tasks to complete
    images = await asyncio.gather(*image_tasks)
    audios = await asyncio.gather(*audio_tasks)
    tts_files = await asyncio.gather(*tts_tasks)
    
    return images, audios, tts_files

# Run async generation
images, audios, tts_files = asyncio.run(generate_assets())

# Create video segments
segments = []
for i, image in enumerate(images):
    segment = video_model.generate_video_segment(
        image_paths=[image],
        audio_path=audios[i] if i < len(audios) else None,
        duration=6.0,
        effects=["stabilization", "color_grade"]
    )
    segments.append(segment)

# Assemble final video
final_video = assembler.assemble_video(
    video_segments=segments,
    tts_audios=tts_files,
    background_audios=audios,
    transitions=["fade", "slide_left", "dissolve"],
    output_file="custom_video.mp4"
)

print(f"Custom video created: {final_video}")
```

This comprehensive API reference provides complete documentation for all VidGen components with practical examples and best practices for implementation.
