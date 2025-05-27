import os
import logging
from typing import Optional

class VideoGenConfig:
    """
    Centralized configuration class for VidGen video generation framework.
    
    This class manages all configuration settings including model parameters,
    file paths, API configurations, and logging settings. It provides
    validation and environment variable support for flexible deployment.
    
    Attributes:
        STABLE_DIFFUSION_MODEL (str): The Stable Diffusion model identifier for image generation
        DEFAULT_SEGMENT_DURATION (int): Default duration in seconds for video segments
        OUTPUT_DIR (str): Base directory for all generated output files
        TEMP_DIR (str): Directory for temporary files during processing
        GEMINI_MODEL (str): Google Gemini model version for script processing
        LOG_LEVEL (int): Logging verbosity level (logging.INFO, DEBUG, etc.)
    """
    # Model settings
    STABLE_DIFFUSION_MODEL = "runwayml/stable-diffusion-v1-5"
    DEFAULT_SEGMENT_DURATION = 5

    # Paths
    OUTPUT_DIR = "outputs"
    TEMP_DIR = "temp"

    # API settings
    GEMINI_MODEL = "gemini-2.0-flash-001"
    LOG_LEVEL = logging.INFO    @classmethod
    def ensure_dirs(cls) -> None:
        """
        Ensure that output and temporary directories exist.
        
        Creates the OUTPUT_DIR and TEMP_DIR directories if they don't exist.
        This method is safe to call multiple times.
        """
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True)

    @classmethod
    def configure_logging(cls) -> None:
        """
        Configure logging with standardized format and level.
        
        Sets up basic logging configuration with timestamp, level, logger name,
        and message formatting. Uses the LOG_LEVEL class attribute to determine
        verbosity.
        """
        logging.basicConfig(
            level=cls.LOG_LEVEL,
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
        )

# For backward compatibility with legacy code
Config = VideoGenConfig
