# VidGen 🎬

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AhmedWGabr/VidGen/tree/main/VidGen.ipynb)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

VidGen is a comprehensive Python framework for automated video generation from text scripts. It combines AI-powered content creation with professional video production capabilities to create engaging videos with minimal manual intervention.

## 🚀 Key Features

### Content Generation
- **AI-Powered Script Analysis**: Advanced script parsing and segmentation using Gemini API
- **Text-to-Speech**: High-quality narration using Bark TTS with voice cloning
- **AI Image Generation**: Dynamic visuals with Stable Diffusion and consistent character appearance
- **Procedural Audio**: Ambient sounds, music generation, and sound effects synthesis

### Video Production
- **Professional Transitions**: Fade, slide, wipe, and custom transition effects
- **Motion Effects**: Zoom, pan, parallax, and camera shake animations
- **Multi-Angle Support**: Dynamic camera angles and perspectives
- **Audio Mixing**: Multi-track audio composition with FFmpeg filters

### Advanced Capabilities
- **Error Recovery System**: Intelligent fallback mechanisms and user-friendly error handling
- **Progress Tracking**: Real-time progress monitoring for long operations
- **Batch Processing**: Efficient handling of multiple video segments
- **Extensible Architecture**: Plugin-ready design for custom effects and generators

## 📋 Requirements

**System Requirements:**
- Python 3.8+
- FFmpeg (for video/audio processing)
- CUDA-compatible GPU (recommended for AI models)
- 8GB+ RAM (16GB+ recommended)

**Key Dependencies:**
- `torch` - Deep learning framework
- `transformers` - NLP and AI models
- `diffusers` - Stable Diffusion image generation
- `bark` - Text-to-speech synthesis
- `ffmpeg-python` - Video/audio processing
- `gradio` - Web-based user interface
- `numpy` - Numerical computing
- `Pillow` - Image processing

See `requirements.txt` for complete dependency list.

## 🏗️ Project Structure

```
VidGen/
├── src/vidgen/              # Main package
│   ├── core/                # Core configuration and exceptions
│   │   ├── config.py        # Configuration management
│   │   └── exceptions.py    # Error handling and recovery
│   ├── models/              # AI and media models
│   │   ├── audio.py         # Audio generation and processing
│   │   ├── image.py         # Image generation with Stable Diffusion
│   │   ├── tts.py           # Text-to-speech with Bark
│   │   └── video.py         # Video effects and transitions
│   ├── services/            # Business logic services
│   │   ├── script_parser.py # Script analysis and segmentation
│   │   └── video_generator.py # Main video generation pipeline
│   ├── ui/                  # User interface
│   │   └── gradio_app.py    # Web interface with Gradio
│   └── utils/               # Utility modules
│       ├── file_manager.py  # File system operations
│       └── logging_config.py # Enhanced logging and progress tracking
├── tests/                   # Comprehensive test suite
│   ├── test_core/          # Core functionality tests
│   ├── test_models/        # Model-specific tests
│   └── test_integration.py # End-to-end integration tests
├── data/                   # Sample data and templates
├── docs/                   # Documentation
├── outputs/                # Generated videos and assets
└── scripts/                # Utility and setup scripts
```

## ⚡ Quick Start

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/AhmedWGabr/VidGen.git
cd VidGen
pip install -e .
```

### 2. Basic Usage

**Web Interface (Recommended):**
```bash
python run_vidgen.py
```
Open your browser to `http://localhost:7860`

**Command Line:**
```bash
python -m src.vidgen.main
```

**Python API:**
```python
from src.vidgen.services.video_generator import VideoGenerator
from src.vidgen.core.config import Config

# Initialize generator
config = Config()
generator = VideoGenerator(config)

# Generate video from script
script = "A beautiful sunset over the mountains..."
video_path = generator.generate_video(
    script=script,
    output_path="outputs/my_video.mp4"
)
```

### 3. Advanced Usage Examples

**Custom Audio Generation:**
```python
from src.vidgen.models.audio import AudioModel

audio_model = AudioModel()

# Generate ambient audio
ambient_audio = audio_model.generate_audio(
    "generate peaceful forest ambient sounds for 30 seconds"
)

# Generate music
music = audio_model.generate_audio(
    "create upbeat electronic music in C major"
)

# Mix multiple audio tracks
mixed_audio = audio_model.mix_audio([ambient_audio, music])
```

**Video Effects and Transitions:**
```python
from src.vidgen.models.video import VideoModel

video_model = VideoModel()

# Add transitions between clips
video_with_transitions = video_model.generate_video_with_transitions(
    image_paths=["img1.jpg", "img2.jpg", "img3.jpg"],
    audio_path="narration.wav",
    transition_type="fade",
    segment_duration=5.0
)

# Add motion effects
dynamic_video = video_model.add_motion_effects(
    video_path="base_video.mp4",
    effect_type="zoom_pan",
    intensity=0.3
)
```

## 🎛️ Configuration

VidGen uses a comprehensive configuration system that can be customized via environment variables or config files:

```python
# src/vidgen/core/config.py
class Config:
    # API Settings
    GEMINI_API_KEY = "your_gemini_api_key"
    HUGGINGFACE_TOKEN = "your_hf_token"
    
    # Model Settings
    IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
    TTS_MODEL = "bark"
    
    # Video Settings
    VIDEO_RESOLUTION = (1920, 1080)
    VIDEO_FPS = 30
    DEFAULT_SEGMENT_DURATION = 5.0
    
    # Audio Settings
    AUDIO_SAMPLE_RATE = 44100
    AUDIO_CHANNELS = 2
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_models/ -v       # Model tests
python -m pytest tests/test_core/ -v         # Core functionality
python -m pytest tests/test_integration.py -v # Integration tests

# Run with coverage
python -m pytest tests/ --cov=src/vidgen --cov-report=html
```

## 🔧 Development

### Setting up Development Environment

```bash
# Clone and setup
git clone https://github.com/AhmedWGabr/VidGen.git
cd VidGen

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Project Guidelines

- **Code Style**: Follow PEP 8, use `black` for formatting
- **Type Hints**: Use type annotations for all public APIs
- **Documentation**: Docstrings for all public functions and classes
- **Testing**: Maintain >90% test coverage
- **Error Handling**: Use the built-in error recovery system

## 📚 API Documentation

### Core Classes

#### VideoGenerator
Main orchestrator for video generation pipeline.

```python
from src.vidgen.services.video_generator import VideoGenerator

generator = VideoGenerator(config)
video_path = generator.generate_video(
    script="Your script here",
    output_path="output.mp4",
    progress_callback=lambda p: print(f"Progress: {p}%")
)
```

#### AudioModel
Advanced audio generation and processing.

```python
from src.vidgen.models.audio import AudioModel

audio = AudioModel()

# Generate procedural audio
audio_path = audio.generate_audio("ambient forest sounds")

# Mix multiple tracks
mixed = audio.mix_audio([track1, track2], volumes=[0.8, 0.5])
```

#### VideoModel
Video effects, transitions, and post-processing.

```python
from src.vidgen.models.video import VideoModel

video = VideoModel()

# Add professional transitions
result = video.generate_video_with_transitions(
    image_paths=images,
    audio_path=audio,
    transition_type="slide_left"
)
```

## 🚨 Error Handling

VidGen includes a comprehensive error recovery system:

```python
from src.vidgen.core.exceptions import with_error_recovery, VidGenError

@with_error_recovery
def my_function():
    # Your code here
    pass

try:
    result = some_operation()
except VidGenError as e:
    print(f"Error: {e}")
    print(f"Suggestion: {e.recovery_suggestion}")
```

## 🔄 Migration Guide

### From Legacy Structure

If you're upgrading from an older version:

1. **Update imports:**
   ```python
   # Old
   from vidgen.audio import generate_audio
   
   # New
   from src.vidgen.models.audio import AudioModel
   audio_model = AudioModel()
   audio_model.generate_audio(...)
   ```

2. **Update configuration:**
   ```python
   # Old
   config = load_config("config.yaml")
   
   # New
   from src.vidgen.core.config import Config
   config = Config()
   ```

3. **Error handling:**
   ```python
   # Old
   try:
       result = generate_video(...)
   except Exception as e:
       print(f"Error: {e}")
   
   # New
   from src.vidgen.core.exceptions import with_error_recovery
   
   @with_error_recovery
   def generate_video_safe(...):
       return generate_video(...)
   ```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Bark** - Text-to-speech synthesis
- **Stable Diffusion** - AI image generation
- **FFmpeg** - Video/audio processing
- **Gradio** - Web interface framework
- **Hugging Face** - Model hosting and transformers library

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/AhmedWGabr/VidGen/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AhmedWGabr/VidGen/discussions)

---

**Made with ❤️ by the VidGen Team**
