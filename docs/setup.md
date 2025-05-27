# VidGen Setup Guide

This comprehensive guide will help you set up and configure the VidGen video generation system for your specific requirements.

## System Requirements

- **Python**: 3.8 or newer (3.9 recommended)
- **Operating Systems**: 
  - Windows 10/11 (64-bit)
  - macOS 11+ (Big Sur or newer)
  - Linux (Ubuntu 20.04+, Debian 11+)
- **Hardware**:
  - **CPU**: Modern multi-core processor (6+ cores recommended)
  - **RAM**: 8GB minimum, 16GB+ recommended for HD video, 32GB+ for 4K
  - **GPU**: NVIDIA GPU with 6GB+ VRAM (strongly recommended)
  - **Storage**: 10GB minimum for installation, 50GB+ recommended for projects
- **External Dependencies**: FFmpeg (4.0+)

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

VidGen requires an API key for Google's Gemini API:

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

Alternatively, create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

## Configuration Options

VidGen can be configured through `vidgen.core.config`. Key settings:

| Setting | Description | Default |
|---------|-------------|---------|
| `STABLE_DIFFUSION_MODEL` | Model path/ID for image generation | `"runwayml/stable-diffusion-v1-5"` |
| `OUTPUT_DIR` | Directory for generated files | `"./outputs"` |
| `TEMP_DIR` | Directory for temporary files | `"./outputs/temp"` |
| `LOG_LEVEL` | Level of logging detail | `"INFO"` |
| `DEFAULT_SEGMENT_DURATION` | Default video segment length | `5` (seconds) |
| `MAX_SEGMENTS` | Maximum number of segments | `20` |
| `AUDIO_SAMPLE_RATE` | Audio sample rate in Hz | `24000` |

You can override these settings programmatically:

```python
from vidgen.core.config import VideoGenConfig

# Override configuration
VideoGenConfig.OUTPUT_DIR = "/custom/output/path"
VideoGenConfig.STABLE_DIFFUSION_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
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
