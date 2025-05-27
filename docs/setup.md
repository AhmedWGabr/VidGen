# VidGen Setup Guide

This comprehensive guide will help you set up and configure the VidGen video generation system for your specific requirements.

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or newer (3.9+ recommended for optimal performance)
- **Operating Systems**: 
  - Windows 10/11 (64-bit)
  - macOS 11+ (Big Sur or newer) 
  - Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- **Hardware**:
  - **CPU**: Quad-core processor (Intel i5/AMD Ryzen 5 or equivalent)
  - **RAM**: 8GB minimum
  - **GPU**: DirectX 11 compatible (integrated graphics acceptable)
  - **Storage**: 15GB available space
- **External Dependencies**: FFmpeg 4.0+

### Recommended Specifications
- **CPU**: 8+ core processor (Intel i7/i9, AMD Ryzen 7/9, or Apple M1/M2/M3)
- **RAM**: 16GB+ (32GB for 4K video processing)
- **GPU**: 
  - NVIDIA RTX 3060+ with 8GB+ VRAM (CUDA support)
  - AMD RX 6700 XT+ with 8GB+ VRAM 
  - Apple M1/M2/M3 with unified memory
- **Storage**: 
  - SSD with 50GB+ free space
  - Additional storage for project files and model cache
- **Network**: Stable internet connection for model downloads and API calls

### Performance Benchmarks
| Hardware Config | HD Video (5min) | 4K Video (5min) | Model Loading |
|----------------|-----------------|-----------------|---------------|
| Minimum (CPU only) | ~45-60 minutes | Not recommended | ~2-3 minutes |
| Mid-range + GPU | ~15-25 minutes | ~35-50 minutes | ~1-2 minutes |
| High-end + RTX 4080+ | ~8-12 minutes | ~15-25 minutes | ~30-60 seconds |

## Installation Options

### Option 1: Installation with pip (Recommended)

```bash
# Create a virtual environment
python -m venv vidgen-env

# Activate the environment
# On Windows:
vidgen-env\Scripts\activate
# On macOS/Linux:
source vidgen-env/bin/activate

# Install VidGen
pip install vidgen

# Or install directly from GitHub for latest development version
pip install git+https://github.com/AhmedWGabr/VidGen.git
```

### Option 2: Manual Installation from Source

```bash
# Clone the repository
git clone https://github.com/AhmedWGabr/VidGen.git
cd VidGen

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install in development mode
pip install -e .

# Additional development dependencies (optional)
pip install -e ".[dev]"
```

### Option 3: Automated Setup Script

The project includes a setup script that automates the installation process:

```bash
# Clone the repository if you haven't already
git clone https://github.com/AhmedWGabr/VidGen.git
cd VidGen

# Run the setup script
python scripts/setup_env.py --with-cuda
```

The script will:
1. Create a virtual environment
2. Install all dependencies
3. Download required ML models
4. Set up FFmpeg (if not already installed)
5. Run validation tests to ensure everything works

## External Dependencies

### FFmpeg Installation

FFmpeg is required for video and audio processing. Here's how to install it:

#### Windows:
1. Download the latest build from [BtbN's FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/releases) (choose `ffmpeg-master-latest-win64-gpl.zip`)
2. Extract the ZIP file to a location like `C:\Program Files\FFmpeg`
3. Add the `bin` directory to your system PATH:
   - Right-click on "This PC" or "My Computer" > Properties > Advanced system settings > Environment Variables
   - Find "Path" under System variables, click Edit
   - Add `C:\Program Files\FFmpeg\bin`
   - Click OK to save
4. Verify installation: open a new Command Prompt and run `ffmpeg -version`

#### macOS:
```bash
# Using Homebrew (recommended)
brew install ffmpeg

# Using MacPorts
sudo port install ffmpeg

# Verify installation
ffmpeg -version
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

#### Linux (Fedora/RHEL/CentOS):
```bash
sudo dnf install ffmpeg

# Verify installation
ffmpeg -version
```

## Model Downloads

VidGen uses several machine learning models which can be pre-downloaded:

```bash
# Download all required models
python -m vidgen.models --download-all

# Or download specific models
python -m vidgen.models --download tts
python -m vidgen.models --download image
```

Models are cached in the following locations:
- Windows: `C:\Users\<username>\.cache\vidgen`
- macOS/Linux: `~/.cache/vidgen`

## API Key Setup

VidGen requires API keys for optimal functionality:

### 🔑 Required: Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or log in to your Google account
3. Generate a new API key
4. Set the API key as an environment variable:

```bash
# Windows (Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:GEMINI_API_KEY = "your_api_key_here"

# macOS/Linux
export GEMINI_API_KEY="your_api_key_here"
```

### 🔐 Optional: Hugging Face Token

For accessing private models or increased rate limits:

1. Visit [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Create a new token with "Read" permissions
3. Set the token as an environment variable:

```bash
# Windows (Command Prompt)
set HUGGINGFACE_TOKEN=your_token_here

# Windows (PowerShell)
$env:HUGGINGFACE_TOKEN = "your_token_here"

# macOS/Linux
export HUGGINGFACE_TOKEN="your_token_here"
```

### 📝 Configuration File

Alternatively, create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
HUGGINGFACE_TOKEN=your_token_here
```

## Configuration Options

VidGen can be configured through the `vidgen.core.config.VideoGenConfig` class. Here are the key settings:

### Core Settings
| Setting | Description | Default | Type |
|---------|-------------|---------|------|
| `OUTPUT_DIR` | Directory for generated files | `"./outputs"` | `str` |
| `TEMP_DIR` | Directory for temporary files | `"./outputs/temp"` | `str` |
| `LOG_LEVEL` | Logging detail level | `"INFO"` | `str` |
| `DEVICE` | Computation device | `"auto"` | `str` |

### Model Configuration
| Setting | Description | Default | Type |
|---------|-------------|---------|------|
| `STABLE_DIFFUSION_MODEL` | Image generation model | `"runwayml/stable-diffusion-v1-5"` | `str` |
| `TTS_MODEL` | Text-to-speech model | `"bark"` | `str` |
| `BARK_MODEL_SIZE` | Bark model variant | `"small"` | `str` |
| `HALF_PRECISION` | Use float16 for memory efficiency | `False` | `bool` |

### Video Settings
| Setting | Description | Default | Type |
|---------|-------------|---------|------|
| `DEFAULT_SEGMENT_DURATION` | Default video segment length (seconds) | `5` | `int` |
| `MAX_SEGMENTS` | Maximum number of segments | `20` | `int` |
| `VIDEO_FPS` | Output video frame rate | `30` | `int` |
| `VIDEO_RESOLUTION` | Output resolution | `"1920x1080"` | `str` |

### Audio Settings
| Setting | Description | Default | Type |
|---------|-------------|---------|------|
| `AUDIO_SAMPLE_RATE` | Audio sample rate in Hz | `24000` | `int` |
| `AUDIO_CHANNELS` | Number of audio channels | `1` | `int` |
| `ENABLE_BACKGROUND_AUDIO` | Include background music | `True` | `bool` |

### Advanced Settings
| Setting | Description | Default | Type |
|---------|-------------|---------|------|
| `USE_STREAMING` | Enable streaming for large videos | `False` | `bool` |
| `AUTO_CLEANUP` | Automatically clean temporary files | `True` | `bool` |
| `SAFETY_CHECKER` | Enable content safety checking | `True` | `bool` |
| `PROGRESS_TRACKING` | Enable detailed progress reporting | `True` | `bool` |

### Configuration Examples

**Basic Configuration:**
```python
from vidgen.core.config import VideoGenConfig

# Set output directory
VideoGenConfig.OUTPUT_DIR = "/custom/output/path"

# Use a different image model
VideoGenConfig.STABLE_DIFFUSION_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

# Enable memory optimization
VideoGenConfig.HALF_PRECISION = True
VideoGenConfig.AUTO_CLEANUP = True
```

**Performance Optimization:**
```python
# For systems with limited VRAM
VideoGenConfig.HALF_PRECISION = True
VideoGenConfig.STABLE_DIFFUSION_MODEL = "runwayml/stable-diffusion-v1-5"  # Smaller model

# For high-end systems
VideoGenConfig.STABLE_DIFFUSION_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
VideoGenConfig.VIDEO_RESOLUTION = "3840x2160"  # 4K
VideoGenConfig.HALF_PRECISION = False  # Full precision for quality

# For batch processing
VideoGenConfig.USE_STREAMING = True
VideoGenConfig.AUTO_CLEANUP = True
```

**Environment Variables:**
You can also configure VidGen using environment variables:

```bash
# Model configuration
export VIDGEN_STABLE_DIFFUSION_MODEL="stabilityai/stable-diffusion-xl-base-1.0"
export VIDGEN_OUTPUT_DIR="/custom/output"
export VIDGEN_DEVICE="cuda"

# Performance settings
export VIDGEN_HALF_PRECISION="true"
export VIDGEN_VIDEO_FPS="60"
export VIDGEN_VIDEO_RESOLUTION="2560x1440"
```

## Environment-Specific Setup

### CUDA Setup for NVIDIA GPUs

For optimal performance with NVIDIA GPUs:

1. Install the [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) (11.6+ recommended)
2. Install the [NVIDIA cuDNN library](https://developer.nvidia.com/cudnn)
3. Install PyTorch with CUDA support:

```bash
# For CUDA 11.8
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch==2.1.0+cu121 torchvision==0.16.0+cu121 --extra-index-url https://download.pytorch.org/whl/cu121
```

Verify CUDA is working:
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
```

### Apple Silicon (M1/M2/M3) Setup

For optimized performance on Apple Silicon:

```bash
# Install PyTorch with MPS support
pip install torch torchvision

# Verify MPS is available
python -c "import torch; print(f'MPS available: {torch.backends.mps.is_available()}')"
```

In your code or configuration:
```python
# Set device to MPS if available
VideoGenConfig.DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
```

### Docker Setup

We provide a Docker image for containerized deployment:

```bash
# Build the Docker image
docker build -t vidgen .

# Run VidGen in a container with GPU support
docker run --gpus all -p 7860:7860 -v $(pwd)/outputs:/app/outputs -e GEMINI_API_KEY=your_key_here vidgen

# Or without GPU
docker run -p 7860:7860 -v $(pwd)/outputs:/app/outputs -e GEMINI_API_KEY=your_key_here vidgen
```

## Verification & Testing

Verify your installation:

```bash
# Run a simple verification
python -m vidgen.core.verify

# Run the test suite
pytest

# Generate a test video with a sample script
python -m vidgen.main --script data/samples/countryside_morning.txt --output test_video.mp4
```

## Troubleshooting

### CUDA/GPU Issues

| Problem | Solution |
|---------|----------|
| `CUDA out of memory` | Reduce batch size or use `--half-precision` flag |
| `CUDA not available` | Check NVIDIA drivers are installed and up-to-date |
| GPU detected but not used | Force GPU: `export CUDA_VISIBLE_DEVICES=0` |

Run the diagnostics tool:
```bash
python -m vidgen.utils.diagnostics --check-gpu
```

### Image Generation Issues

| Problem | Solution |
|---------|----------|
| Black or corrupted images | Check VRAM, try: `VideoGenConfig.STABLE_DIFFUSION_SAFETY_CHECKER = False` |
| Images too similar | Try different prompts or increase the guidance scale |
| Generation too slow | Try a smaller model or enable `--half-precision` |

### TTS (Text-to-Speech) Issues

| Problem | Solution |
|---------|----------|
| Robotic/distorted audio | Check sample rate matches your output device |
| No audio generated | Check if Bark is installed correctly |
| Slow generation | Consider using a faster TTS model or pre-caching voices |

### FFmpeg Issues

| Problem | Solution |
|---------|----------|
| `FFmpeg not found` | Ensure FFmpeg is in PATH or set `VideoGenConfig.FFMPEG_PATH` |
| `Unknown encoder` | Install FFmpeg with additional codecs |
| Video assembly failing | Check FFmpeg version (`ffmpeg -version`) is 4.0+ |

### Memory Usage Optimization

If you're experiencing memory issues:

1. Use streaming for large videos:
   ```python
   VideoGenConfig.USE_STREAMING = True
   ```

2. Process segments individually:
   ```python
   VideoGenConfig.SEGMENT_PROCESSING = "individual"
   ```

3. Enable automatic cleanup:
   ```python
   VideoGenConfig.AUTO_CLEANUP = True
   ```

4. Reduce model precision:
   ```python
   VideoGenConfig.HALF_PRECISION = True  # Uses float16 instead of float32
   ```

## Getting Help

If you encounter issues not covered by this guide:

1. Check the [FAQ](https://github.com/AhmedWGabr/VidGen/wiki/FAQ) in the wiki
2. Look for similar issues in the [GitHub Issues](https://github.com/AhmedWGabr/VidGen/issues)
3. Run the diagnostics tool: `python -m vidgen.utils.diagnostics --full`
4. Join our [Discord community](https://discord.gg/vidgen) for real-time help

If you need to report an issue, please include the diagnostics report.
