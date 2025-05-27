#!/usr/bin/env python3
"""
VidGen Colab Setup Script
=========================

This script sets up the VidGen environment for Google Colab usage.
It handles GPU detection, dependency installation, and environment configuration.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

def setup_logging():
    """Configure logging for setup process."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('VidGen.setup')

def check_gpu():
    """Check if GPU is available in Colab."""
    logger = logging.getLogger('VidGen.setup')
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            logger.info(f"GPU detected: {gpu_name}")
            return True
        else:
            logger.warning("No GPU detected. Performance will be limited.")
            return False
    except ImportError:
        logger.warning("PyTorch not installed yet. GPU check will be performed after installation.")
        return False

def install_system_dependencies():
    """Install system-level dependencies for Colab."""
    logger = logging.getLogger('VidGen.setup')
    
    # Install FFmpeg (essential for video processing)
    logger.info("Installing FFmpeg...")
    try:
        subprocess.run(['apt-get', 'update', '-qq'], check=True)
        subprocess.run(['apt-get', 'install', '-y', 'ffmpeg'], check=True)
        logger.info("FFmpeg installed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install FFmpeg: {e}")
        
    # Install other system dependencies
    logger.info("Installing additional system dependencies...")
    try:
        subprocess.run(['apt-get', 'install', '-y', 'libsndfile1'], check=True)
        logger.info("System dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        logger.warning(f"Some system dependencies failed to install: {e}")

def install_python_dependencies():
    """Install Python dependencies optimized for Colab."""
    logger = logging.getLogger('VidGen.setup')
    
    # Core dependencies for Colab
    colab_requirements = [
        'torch>=2.0.0',
        'torchvision>=0.15.0',
        'diffusers>=0.21.0',
        'transformers>=4.30.0',
        'accelerate>=0.20.0',
        'bark',
        'gradio>=3.35.0',
        'requests>=2.28.0',
        'pillow>=9.0.0',
        'numpy>=1.21.0',
        'opencv-python>=4.5.0',
        'scipy>=1.7.0',
        'librosa>=0.9.0',
        'soundfile>=0.10.0',
        'pydantic>=1.10.0',
        'google-generativeai>=0.3.0',
        'moviepy>=1.0.3',
        'tqdm>=4.64.0'
    ]
    
    logger.info("Installing Python dependencies for Colab...")
    for package in colab_requirements:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         check=True, capture_output=True)
            logger.info(f"Installed: {package}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to install {package}: {e}")

def setup_environment():
    """Set up environment variables and directories for Colab."""
    logger = logging.getLogger('VidGen.setup')
    
    # Create necessary directories
    directories = [
        '/content/vidgen/outputs',
        '/content/vidgen/outputs/audio',
        '/content/vidgen/outputs/images', 
        '/content/vidgen/outputs/videos',
        '/content/vidgen/outputs/temp',
        '/content/vidgen/models'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    # Set environment variables for Colab
    os.environ['TRANSFORMERS_CACHE'] = '/content/vidgen/models'
    os.environ['HF_HOME'] = '/content/vidgen/models'
    os.environ['TORCH_HOME'] = '/content/vidgen/models'
    
    logger.info("Environment variables configured for Colab")

def install_vidgen():
    """Install VidGen package in development mode."""
    logger = logging.getLogger('VidGen.setup')
    
    try:
        # Install in development mode for Colab
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', '.'], 
                      check=True, cwd='/content/VidGen')
        logger.info("VidGen installed successfully in development mode")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install VidGen: {e}")

def verify_installation():
    """Verify that the installation is working correctly."""
    logger = logging.getLogger('VidGen.setup')
    
    try:
        # Test basic imports
        import torch
        import diffusers
        import transformers
        import gradio
        logger.info("✅ Core dependencies imported successfully")
        
        # Test VidGen imports
        from vidgen.core.config import VideoGenConfig
        from vidgen.models.audio import generate_background_audio
        from vidgen.models.image import generate_character_image
        logger.info("✅ VidGen modules imported successfully")
        
        # Check GPU availability
        if torch.cuda.is_available():
            logger.info(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
        else:
            logger.warning("⚠️ No GPU detected - performance will be limited")
            
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False

def setup_api_keys():
    """Guide user through API key setup for Colab."""
    logger = logging.getLogger('VidGen.setup')
    
    logger.info("=" * 50)
    logger.info("API KEY SETUP REQUIRED")
    logger.info("=" * 50)
    logger.info("To use VidGen, you need to set up API keys:")
    logger.info("1. Get a Google Gemini API key from: https://makersuite.google.com/")
    logger.info("2. In Colab, add it to Secrets with name 'GEMINI_API_KEY'")
    logger.info("3. Or set it in your code: os.environ['GEMINI_API_KEY'] = 'your-key'")
    logger.info("=" * 50)

def main():
    """Main setup function for VidGen in Google Colab."""
    logger = setup_logging()
    
    logger.info("🚀 Setting up VidGen for Google Colab...")
    
    # Check if we're in Colab
    try:
        import google.colab
        logger.info("✅ Running in Google Colab environment")
    except ImportError:
        logger.warning("⚠️ Not running in Colab - some features may not work")
    
    # Setup steps
    logger.info("📦 Installing system dependencies...")
    install_system_dependencies()
    
    logger.info("🐍 Installing Python dependencies...")
    install_python_dependencies()
    
    logger.info("📁 Setting up environment...")
    setup_environment()
    
    logger.info("⚙️ Installing VidGen...")
    install_vidgen()
    
    logger.info("🔍 Verifying installation...")
    if verify_installation():
        logger.info("✅ VidGen setup completed successfully!")
        setup_api_keys()
    else:
        logger.error("❌ Setup failed - please check error messages above")
    
    logger.info("🎬 VidGen is ready to use in Colab!")

if __name__ == "__main__":
    main()
