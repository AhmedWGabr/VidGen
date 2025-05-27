# File operations

import os
import uuid
import atexit
import logging
import tempfile
from vidgen.core.config import VideoGenConfig

logger = logging.getLogger("VidGen.utils.file_manager")

# Store temporary files to be cleaned up at exit
_temp_files = []

def get_temp_dir():
    """Get the temporary directory path, ensuring it exists."""
    temp_dir = os.path.join(VideoGenConfig.OUTPUT_DIR, VideoGenConfig.TEMP_DIR)
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def get_output_dir(subdir=None):
    """
    Get an output directory path, creating it if it doesn't exist.
    
    Args:
        subdir (str): Optional subdirectory inside the main output dir
        
    Returns:
        str: Path to the output directory
    """
    if subdir:
        output_dir = os.path.join(VideoGenConfig.OUTPUT_DIR, subdir)
    else:
        output_dir = VideoGenConfig.OUTPUT_DIR
    
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def generate_unique_filename(prefix="", suffix="", directory=None):
    """
    Generate a unique filename with optional prefix and suffix.
    
    Args:
        prefix (str): Optional prefix for the filename
        suffix (str): Optional suffix for the filename (extension)
        directory (str): Directory to create the file in, defaults to temp dir
        
    Returns:
        str: Unique filename path
    """
    directory = directory or get_temp_dir()
    unique_id = uuid.uuid4().hex
    return os.path.join(directory, f"{prefix}{unique_id}{suffix}")

def register_temp_file(file_path):
    """
    Register a file to be cleaned up when the application exits.
    
    Args:
        file_path (str): Path to the file to clean up
    """
    global _temp_files
    _temp_files.append(file_path)
    return file_path

def cleanup_temp_files():
    """Clean up all registered temporary files."""
    for file_path in _temp_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up file {file_path}: {e}")

# Register cleanup function to run at exit
atexit.register(cleanup_temp_files)
