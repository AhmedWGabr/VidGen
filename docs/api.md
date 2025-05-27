# VidGen API Documentation

This document provides a comprehensive reference for the VidGen package, explaining the purpose, usage, and relationships between components.

## Package Structure

VidGen is organized into the following main modules:

```
vidgen/
├── core/           # Core configuration and shared components
├── models/         # ML model interfaces and abstractions  
├── services/       # Business logic and processing
├── ui/             # User interface components
└── utils/          # Utility functions and helpers
```

## Core Components

### Configuration (`vidgen.core.config`)

Central configuration management for the entire application.

```python
from vidgen.core.config import VideoGenConfig

# Access configuration values
output_dir = VideoGenConfig.OUTPUT_DIR 
stable_diffusion_model = VideoGenConfig.STABLE_DIFFUSION_MODEL

# Set configuration values
VideoGenConfig.OUTPUT_DIR = "custom/output/path"
```

### Exceptions (`vidgen.core.exceptions`)

Custom exception classes for more specific error handling.

```python
from vidgen.core.exceptions import ScriptParsingError, ModelLoadError

try:
    # Some operation
    pass
except ScriptParsingError as e:
    # Handle script parsing specific error
    print(f"Script error: {e}")
```

## Service Components

### Script Parsing (`vidgen.services.script_parser`)

The script parsing module handles converting user-provided scripts or API responses into structured data for video generation.

```python
from vidgen.services.script_parser import parse_detailed_script, validate_segment

# Parse a detailed script from the Gemini API
parsed_data = parse_detailed_script(detailed_script_json)

# Access different components
video_commands = parsed_data["video"]  # List of video segment commands
tts_commands = parsed_data["tts"]      # List of text-to-speech narration commands
audio_commands = parsed_data["audio"]  # List of background audio commands
image_commands = parsed_data["image"]  # List of character/image generation commands

# Validate a single script segment
segment = {"start": 0, "end": 5, "narration": "Hello world"}
validate_segment(segment)  # Raises ValueError if invalid
```

### Gemini API Integration (`vidgen.services.gemini_api`)

Handles communication with Google's Gemini API for script generation and enhancement.

```python
from vidgen.services.gemini_api import generate_script, enhance_script

# Generate a new script based on a prompt
script = generate_script("A short video about space exploration")

# Enhance an existing basic script with more details
enhanced_script = enhance_script(basic_script)
```

### Video Assembly (`vidgen.services.video_assembler`)

Combines all generated assets (video segments, audio, images) into a final video.

```python
from vidgen.services.video_assembler import assemble_video, apply_effects

# Assemble the final video
output_path = assemble_video(
    video_segments=video_paths,
    tts_audios=tts_audio_paths,
    background_audios=background_audio_paths,
    output_file="final_video.mp4"
)

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

## UI Components

### Gradio App (`vidgen.ui.gradio_app`)

Web interface for the video generation system.

```python
from vidgen.ui.gradio_app import create_ui, start_server

# Create the UI components
ui = create_ui()

# Start the web server
start_server(ui, port=8080)
```

### UI Components (`vidgen.ui.components`)

Reusable UI components and widgets.

```python
from vidgen.ui.components import create_script_editor, create_preview_player

# Create specific UI components for embedding
editor = create_script_editor(default_text="Enter your script here...")
player = create_preview_player()
```

## Utilities

### File Management (`vidgen.utils.file_manager`)

Handle temporary files and directories with automatic cleanup.

```python
from vidgen.utils.file_manager import (
    get_temp_dir, 
    get_output_dir,
    generate_unique_filename,
    register_temp_file,
    cleanup_temp_files
)

# Get or create directories
temp_dir = get_temp_dir()
image_dir = get_output_dir("images")

# Generate a unique filename
unique_path = generate_unique_filename(
    prefix="video_",
    suffix=".mp4",
    directory=temp_dir
)

# Register a temporary file for automatic cleanup
temp_file = register_temp_file("/path/to/temp.mp4")

# Manual cleanup (usually handled automatically)
cleanup_temp_files()
```

### Logging Configuration (`vidgen.utils.logging_config`)

Advanced logging setup with file and console outputs.

```python
from vidgen.utils.logging_config import configure_logging

# Configure logging with console and file output
logger = configure_logging(
    log_to_file=True,
    log_level="DEBUG",
    log_file="vidgen.log"
)

# Use the logger
logger.info("Starting video generation")
logger.debug("Processing script segment")
```

### Helper Functions (`vidgen.utils.helpers`)

Miscellaneous helper functions.

```python
from vidgen.utils.helpers import format_timestamp, extract_metadata, parse_duration

# Format a timestamp for display
formatted = format_timestamp(65.5)  # "01:05.5"

# Extract metadata from a media file
metadata = extract_metadata("video.mp4")  # {duration: 120, width: 1920, ...}

# Parse a duration string to seconds
seconds = parse_duration("1:30")  # 90.0
```
