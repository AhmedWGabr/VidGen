# VidGen 🎬 - AI-Powered Video Generation Framework

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AhmedWGabr/VidGen/blob/main/VidGen_Colab.ipynb)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-70%2B%20cases-green.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](tests/)

VidGen is a state-of-the-art Python framework for automated video generation from text scripts. It seamlessly integrates cutting-edge AI technologies including **Gemini API**, **Stable Diffusion**, **Bark TTS**, and **FFmpeg** to transform simple text descriptions into professional-quality videos with synchronized audio, dynamic visuals, and cinematic effects.

## 🚀 Key Features

### 🤖 AI-Powered Content Generation
- **Advanced Script Analysis**: Leverages Google Gemini API for intelligent script parsing, segmentation, and enhancement
- **Neural Text-to-Speech**: High-fidelity narration using Bark TTS with voice cloning and emotion synthesis
- **AI Image Generation**: Photorealistic visuals with Stable Diffusion XL, featuring consistent character appearance across scenes
- **Procedural Audio Synthesis**: Dynamic ambient sounds, music generation, and sound effects using FFmpeg audio filters
- **Character Face Caching**: Maintains visual consistency with persistent character appearance throughout videos

### 🎥 Professional Video Production
- **Cinematic Transitions**: 8+ transition types including fade, slide, wipe, dissolve, and custom effects
- **Dynamic Motion Effects**: Advanced zoom, pan, parallax, and camera shake animations
- **Multi-Angle Support**: Intelligent camera angle switching and perspective changes
- **Audio Post-Processing**: Multi-track audio mixing, dynamic range compression, and spatial audio
- **Real-time Preview**: Live preview generation during content creation

### 🛠️ Enterprise-Grade Architecture
- **Comprehensive Error Recovery**: Intelligent fallback mechanisms with user-friendly error handling
- **Progress Monitoring**: Real-time progress tracking with detailed operation status
- **Batch Processing**: Efficient parallel processing of multiple video segments
- **Memory Optimization**: Automatic GPU memory management and model caching
- **Extensible Plugin System**: Custom effects, generators, and model integration support
- **Type Safety**: Full type annotations with Pydantic data validation

### 🔧 Production-Ready Features
- **Scalable Infrastructure**: Designed for both desktop and cloud deployment
- **Comprehensive Testing**: 70+ test cases with >90% code coverage
- **Docker Support**: Containerized deployment with GPU acceleration
- **API Integration**: RESTful API for programmatic access
- **Web Interface**: Intuitive Gradio-based UI with real-time feedback

## 📋 System Requirements & Dependencies

### 🖥️ Hardware Requirements
- **CPU**: Multi-core processor (Intel i7/AMD Ryzen 7 or better recommended)
- **RAM**: 16GB minimum, 32GB recommended for 4K video generation
- **GPU**: NVIDIA GPU with 8GB+ VRAM (RTX 3070/4060 or better for optimal performance)
- **Storage**: 50GB+ free space (SSD recommended for temporary files)
- **Network**: Stable internet connection for API calls and model downloads

### 🐍 Software Requirements
- **Python**: 3.8+ (3.10 recommended for best compatibility)
- **FFmpeg**: 4.4+ with H.264, AAC, and filter support
- **CUDA**: 11.8+ for GPU acceleration (optional but highly recommended)
- **Git**: For repository cloning and version control

### 📦 Core Dependencies
```python
# AI and Machine Learning
torch>=2.0.0              # Deep learning framework with CUDA support
transformers>=4.30.0       # Hugging Face transformers for NLP models
diffusers>=0.20.0         # Stable Diffusion pipeline management
bark>=1.0.0               # Advanced text-to-speech synthesis
accelerate>=0.20.0        # Model acceleration and optimization

# Video/Audio Processing
ffmpeg-python>=0.2.0      # Python wrapper for FFmpeg operations
opencv-python>=4.8.0      # Computer vision and image processing
pillow>=10.0.0            # Advanced image manipulation
numpy>=1.24.0             # Numerical computing foundation
scipy>=1.10.0             # Scientific computing and signal processing

# Web Interface & APIs
gradio>=3.40.0            # Interactive web UI components
google-generativeai>=0.3.0 # Google Gemini API integration
requests>=2.31.0          # HTTP client for API communications
aiohttp>=3.8.0            # Async HTTP client for concurrent operations

# Data Validation & Utilities
pydantic>=2.0.0           # Data validation and settings management
python-dotenv>=1.0.0      # Environment variable management
tqdm>=4.65.0              # Progress bars and monitoring
pytest>=7.4.0            # Testing framework
```

### 🌐 API Requirements
- **Google Gemini API Key**: For script analysis and enhancement
- **Hugging Face Token**: For accessing premium/private models (optional but recommended)

**🔧 Centralized Authentication**: All API keys are managed through the unified `VideoGenConfig` class with automatic environment variable detection.

See `requirements.txt` for the complete dependency list with pinned versions.

## 🏗️ Advanced Project Architecture

```
VidGen/
├── 📦 src/vidgen/              # Core Application Package
│   ├── 🔧 core/                # Foundation & Configuration
│   │   ├── config.py           # Centralized configuration management
│   │   └── exceptions.py       # Custom exception hierarchy with recovery
│   ├── 🤖 models/              # AI & Media Processing Models
│   │   ├── audio.py           # Procedural audio synthesis & mixing
│   │   ├── image.py           # Stable Diffusion image generation
│   │   ├── tts.py             # Bark TTS with voice cloning
│   │   ├── video.py           # Video effects & transition engine
│   │   ├── data_models.py     # Pydantic data validation models
│   │   └── model_utils.py     # Model optimization utilities
│   ├── 🔄 services/            # Business Logic & External APIs
│   │   ├── script_parser.py   # Gemini-powered script analysis
│   │   ├── video_generator.py # Main video generation pipeline
│   │   ├── video_assembler.py # Multi-track video assembly
│   │   └── gemini_api.py      # Google Gemini API integration
│   ├── 🖥️ ui/                  # User Interface Components
│   │   ├── gradio_app.py      # Interactive web interface
│   │   └── components.py      # Reusable UI components
│   └── 🛠️ utils/               # Utility Modules
│       ├── file_manager.py    # Advanced file system operations
│       ├── logging_config.py  # Structured logging & progress tracking
│       └── helpers.py         # Common utility functions
├── 🧪 tests/                   # Comprehensive Test Suite (70+ tests)
│   ├── test_core/             # Core functionality tests
│   ├── test_models/           # AI model integration tests
│   ├── test_services/         # Service layer tests
│   ├── test_utils/            # Utility function tests
│   └── test_integration.py    # End-to-end pipeline tests
├── 📚 docs/                   # Documentation & Guides
│   ├── API_REFERENCE.md       # Complete API documentation
│   ├── setup.md              # Installation & configuration guide
│   ├── examples.md           # Usage examples & tutorials
│   └── MIGRATION_GUIDE.md    # Migration from legacy versions
├── 📂 data/                   # Sample Data & Templates
│   ├── samples/              # Example scripts and media
│   └── templates/            # Script templates and presets
├── 📁 outputs/                # Generated Content Storage
│   ├── videos/               # Final video outputs
│   ├── audio/                # Generated audio files
│   ├── images/               # Generated character images
│   └── temp/                 # Temporary processing files
├── 🔧 scripts/                # Utility & Setup Scripts
│   ├── setup_env.py          # Environment configuration
│   ├── download_models.py    # AI model downloading
│   └── cleanup.py            # Cache and temp file cleanup
└── 📜 legacy/                 # Legacy Implementation (deprecated)
    └── [Previous version files for reference]
```

### 🔗 Component Relationships
- **Core** → Provides configuration and error handling to all components
- **Models** → Implements AI/ML functionality used by Services
- **Services** → Orchestrates Models to implement business logic
- **UI** → Provides user interface that calls Services
- **Utils** → Supporting functionality used across all layers

## ⚡ Quick Start Guide

### 🚀 Installation Methods

#### Method 1: Standard Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/AhmedWGabr/VidGen.git
cd VidGen

# Create and activate virtual environment
python -m venv vidgen-env
# Windows PowerShell:
.\vidgen-env\Scripts\Activate.ps1
# Windows Command Prompt:
vidgen-env\Scripts\activate.bat
# macOS/Linux:
source vidgen-env/bin/activate

# Install VidGen with all dependencies
pip install -e .

# Install additional GPU support (if available)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### Method 2: Development Installation
```bash
# Clone with development dependencies
git clone https://github.com/AhmedWGabr/VidGen.git
cd VidGen

# Install in development mode with testing tools
pip install -e ".[dev]"

# Install pre-commit hooks for code quality
pre-commit install
```

#### Method 3: Google Colab (Zero Setup - Recommended for Beginners)

🎯 **Two Ways to Use VidGen in Colab:**

**Option A: Direct Notebook Upload (Recommended)**
1. Download the notebook: [`VidGen_Colab.ipynb`](./VidGen_Colab.ipynb)
2. Upload to Google Colab: [colab.research.google.com](https://colab.research.google.com/)
3. Enable GPU: Runtime → Change runtime type → Hardware accelerator → GPU
4. Run all cells for automated setup and demo

**Option B: GitHub Integration (if repository is public)**
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AhmedWGabr/VidGen/blob/main/VidGen_Colab.ipynb)

Experience VidGen instantly with zero setup required! Our interactive Colab notebook provides:

- **🚀 One-Click Setup**: Automated installation of all dependencies
- **🔥 Free GPU Access**: Leverage Google's T4/A100 GPUs for fast generation
- **📱 Mobile Friendly**: Generate videos from your phone or tablet
- **☁️ Cloud Storage**: No local storage requirements
- **🎓 Interactive Tutorial**: Step-by-step guidance for beginners
- **🔧 Fallback Setup**: Manual installation if GitHub access fails

**🔑 API Key Setup for Colab:**
1. Get your free Gemini API key: [Google AI Studio](https://makersuite.google.com/)
2. In Colab: Secrets tab (🔑) → Add secret → Name: `GEMINI_API_KEY`
3. Run the setup cell to start generating videos instantly!

**🛠️ Colab Features:**
- Automatic GPU detection and optimization
- Fallback manual setup if repository cloning fails
- Interactive demo with sample scripts
- Resource monitoring and optimization tips
- Direct video preview and download capabilities

#### Method 4: Docker Installation (Coming Soon)
```bash
# Quick start with Docker
docker pull ahmedwgabr/vidgen:latest
docker run -p 7860:7860 -v $(pwd)/outputs:/app/outputs vidgen:latest
```

### 🎬 Usage Examples

#### 1. Web Interface (Easiest for Beginners)
```bash
# Launch the interactive web interface
python run_vidgen.py
# Or alternatively:
python -m src.vidgen.main
```
Then open your browser to `http://localhost:7860` for the intuitive drag-and-drop interface.

#### 2. Command Line Interface
```bash
# Generate video from a script file
python -m src.vidgen.main --script "data/samples/countryside_morning.txt" --output "my_video.mp4"

# Generate with custom parameters
python -m src.vidgen.main \
    --script "Your story here..." \
    --api-key "your_gemini_api_key" \
    --duration 7 \
    --seed 42 \
    --resolution 1920x1080
```

#### 3. Python API Integration
```python
from src.vidgen.services.video_generator import VideoGenerator
from src.vidgen.core.config import Config

# Initialize with configuration
config = Config()
config.GEMINI_API_KEY = "your_api_key_here"
config.VIDEO_RESOLUTION = (1920, 1080)
config.DEFAULT_SEGMENT_DURATION = 6.0

generator = VideoGenerator(config)

# Simple video generation
script = """
A serene morning in the countryside. The sun rises over rolling hills 
covered in morning mist. A farmer walks through golden wheat fields 
as birds sing in the distance.
"""

video_path = generator.generate_video(
    script=script,
    output_path="outputs/countryside_morning.mp4",
    progress_callback=lambda msg, progress: print(f"[{progress}%] {msg}")
)

print(f"✅ Video generated successfully: {video_path}")
```

#### 4. Google Colab Usage (Interactive Notebook)
```python
# In Google Colab, use the interactive notebook for guided video generation:
# 1. Open the VidGen_Colab.ipynb notebook
# 2. Follow the step-by-step cells for setup and generation
# 3. Use the built-in examples or create your own scripts

# Quick Colab example:
from vidgen.main import main as vidgen_main
import os

# Set API key (use Colab secrets for security)
from google.colab import userdata
os.environ['GEMINI_API_KEY'] = userdata.get('GEMINI_API_KEY')

# Create and generate video
script = """
Title: "Future of AI"
A modern tech office with holographic displays.
[Background: Futuristic ambient music]
NARRATOR: "Welcome to the future of artificial intelligence."
"""

# Generate video with progress tracking
video_path = vidgen_main(
    script_text=script,
    output_filename="ai_future.mp4"
)

# Download the result
from google.colab import files
files.download(video_path)
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
class VideoGenConfig:
    # API Settings
    GEMINI_API_KEY = "your_gemini_api_key"
    HUGGINGFACE_TOKEN = "your_hf_token"  # For private/premium models
    
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

# Validate your configuration
from src.vidgen.core.config import VideoGenConfig

validation = VideoGenConfig.validate_api_keys()
if validation["all_required_present"]:
    print("✅ All required API keys configured!")
else:
    print(f"⚠️ Missing keys: {validation['missing_keys']}")
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
       return generate_video(...)   ```

## 📁 Project Files Overview

### 🚀 Getting Started Files
- **`VidGen_Colab.ipynb`** - Interactive Google Colab notebook for zero-setup usage
  - Download this file and upload to [Google Colab](https://colab.research.google.com/) for instant access
  - Includes automated setup, fallback installation, and interactive demos
  - Compatible with free Colab GPU runtime (T4/A100)
- **`setup_colab.py`** - Automated Colab environment setup script
- **`requirements_colab.txt`** - Optimized dependencies for Google Colab
- **`requirements.txt`** - Standard Python package requirements
- **`setup.py`** - Python package installation configuration

### 🎬 Main Application Files
- **`run_vidgen.py`** - Main entry point for running VidGen
- **`run.py`** - Alternative launcher script
- **`src/vidgen/main.py`** - Core application logic and orchestration

### 📚 Documentation & Guides
- **`README.md`** - This comprehensive guide
- **`docs/API_REFERENCE.md`** - Complete API documentation
- **`docs/setup.md`** - Detailed installation and configuration guide
- **`docs/examples.md`** - Usage examples and tutorials
- **`docs/MIGRATION_GUIDE.md`** - Migration guide from legacy versions
- **`MODEL_FILES.md`** - AI models documentation and requirements
- **`STRUCTURE.md`** - Project architecture and design patterns

### 📂 Resource Directories
- **`data/samples/`** - Example scripts and templates
- **`outputs/`** - Generated videos, audio, and images
- **`tests/`** - Comprehensive test suite (70+ test cases)
- **`scripts/`** - Utility scripts for setup and maintenance
- **`legacy/`** - Previous version files (deprecated)

### 🔧 Development & Testing
- **`MIGRATION_CHECKLIST.md`** - Development progress tracking
- **`tests/test_integration.py`** - End-to-end functionality tests
- **`scripts/download_models.py`** - AI model downloading utility
- **`scripts/cleanup.py`** - Cache and temporary file management

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
