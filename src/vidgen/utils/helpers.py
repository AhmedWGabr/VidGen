# Utility functions

import os
import json
import hashlib
import time
import logging
from vidgen.core.config import VideoGenConfig

logger = logging.getLogger("VidGen.utils.helpers")

def create_deterministic_seed(text, seed_base=42):
    """
    Create a deterministic seed from text for reproducible generation.
    
    Args:
        text (str): Input text to derive seed from
        seed_base (int): Base seed to combine with text hash
        
    Returns:
        int: Deterministic seed value
    """
    if not text:
        return seed_base
    
    # Create a hash of the text
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    
    # Convert first 8 chars of hash to int and combine with base seed
    hash_int = int(text_hash[:8], 16)
    return (hash_int + seed_base) % (2**32)

def ensure_dirs():
    """Ensure all required directories exist."""
    # Create main output and temp directories
    os.makedirs(VideoGenConfig.OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(VideoGenConfig.OUTPUT_DIR, VideoGenConfig.TEMP_DIR), exist_ok=True)
    
    # Create subdirectories for different types of output
    output_subdirs = ["videos", "images", "audio"]
    for subdir in output_subdirs:
        os.makedirs(os.path.join(VideoGenConfig.OUTPUT_DIR, subdir), exist_ok=True)
    
    # Create logging directory
    os.makedirs(os.path.join(VideoGenConfig.OUTPUT_DIR, "logs"), exist_ok=True)

def load_json_safe(text):
    """
    Safely load JSON from text, handling common errors.
    
    Args:
        text (str): JSON text to load
        
    Returns:
        dict/list: Parsed JSON data or None if invalid
    """
    if not text:
        return None
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {e}")
        
        # Try to extract JSON from the text if it contains non-JSON preamble or postscript
        try:
            # Look for JSON in case Gemini wraps the response in other text
            start_idx = text.find('[')
            end_idx = text.rfind(']') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                potential_json = text[start_idx:end_idx]
                return json.loads(potential_json)
        except:
            pass
        
        return None

def format_time(seconds):
    """
    Format seconds into a human-readable time string.
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Formatted time string (MM:SS)
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
