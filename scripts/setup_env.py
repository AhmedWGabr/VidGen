#!/usr/bin/env python3
"""
Setup script for VidGen development environment.
This script helps set up the development environment with proper dependencies.
"""

import os
import sys
import subprocess
import logging
import platform
from pathlib import Path

# Root directory (parent of script directory)
ROOT_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def setup_logging():
    """Set up logging for the setup script"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

# Initialize logger
logger = setup_logging()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        raise RuntimeError("Python 3.8 or higher is required")
    print(f"✓ Python {sys.version.split()[0]} is compatible")

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("FFmpeg is installed")
            return True
        else:
            logger.warning("FFmpeg test command failed")
            return False
    except Exception:
        logger.warning("FFmpeg is not installed or not in PATH")
        return False

def install_python_dependencies():
    """Install Python dependencies from requirements.txt."""
    try:
        logger.info("Installing Python dependencies...")
        
        # Check if we're in a virtual environment
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        if not in_venv:
            logger.warning("Not running in a virtual environment. It's recommended to use a virtual environment.")
        
        # Install dependencies
        requirements_path = ROOT_DIR / "requirements.txt"
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_path)])
        
        # Install the package in development mode
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', str(ROOT_DIR)])
        
        logger.info("Python dependencies installed successfully")
        return True
    except Exception as e:
        logger.error(f"Error installing Python dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories for the project."""
    try:
        logger.info("Creating project directories...")
        
        dirs = [
            ROOT_DIR / "outputs",
            ROOT_DIR / "outputs/videos",
            ROOT_DIR / "outputs/audio",
            ROOT_DIR / "outputs/images",
            ROOT_DIR / "outputs/temp",
            ROOT_DIR / "outputs/logs",
            ROOT_DIR / "data/samples",
            ROOT_DIR / "data/templates",
        ]
        
        for directory in dirs:
            directory.mkdir(exist_ok=True, parents=True)
            logger.debug(f"Created directory: {directory}")
        
        logger.info("Project directories created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating directories: {e}")
        return False

def download_models():
    """Download ML models by calling the download_models.py script."""
    try:
        logger.info("Downloading ML models...")
        download_script = ROOT_DIR / "scripts" / "download_models.py"
        subprocess.check_call([sys.executable, str(download_script)])
        logger.info("Models downloaded successfully")
        return True
    except Exception as e:
        logger.error(f"Error downloading models: {e}")
        return False

def main():
    """Run the complete setup process."""
    logger.info("Starting VidGen environment setup")
    
    # Check system information
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    
    # Create project directories
    if not create_directories():
        logger.warning("Failed to create some directories")
    
    # Check for FFmpeg
    if not check_ffmpeg():
        logger.warning("FFmpeg is required but not found. Please install FFmpeg before using VidGen.")
    
    # Install Python dependencies
    if not install_python_dependencies():
        logger.error("Failed to install Python dependencies")
        return 1
    
    # Download models
    if not download_models():
        logger.warning("Failed to download some models")
    
    logger.info("VidGen environment setup completed")
    logger.info("You can now run VidGen with 'python run.py'")
    return 0

if __name__ == "__main__":
    sys.exit(main())
