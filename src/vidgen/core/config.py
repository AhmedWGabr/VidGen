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
        GEMINI_API_KEY (str): Google Gemini API key for script processing
        HUGGINGFACE_TOKEN (str): Hugging Face token for model authentication
        LOG_LEVEL (int): Logging verbosity level (logging.INFO, DEBUG, etc.)
    """
    # Model settings
    STABLE_DIFFUSION_MODEL = "runwayml/stable-diffusion-v1-5"
    DEFAULT_SEGMENT_DURATION = 5

    # Paths
    OUTPUT_DIR = "outputs"
    TEMP_DIR = "temp"    # API settings
    GEMINI_MODEL = "gemini-2.0-flash-001"
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
    LOG_LEVEL = logging.INFO

    @classmethod
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

    @classmethod
    def validate_api_keys(cls) -> dict:
        """
        Validate that required API keys are configured.
        
        Returns:
            dict: Validation results with status and missing keys
        """
        validation_results = {
            "gemini_api_key": bool(cls.GEMINI_API_KEY),
            "huggingface_token": bool(cls.HUGGINGFACE_TOKEN),
            "missing_keys": []
        }
        
        if not cls.GEMINI_API_KEY:
            validation_results["missing_keys"].append("GEMINI_API_KEY")
        
        if not cls.HUGGINGFACE_TOKEN:
            validation_results["missing_keys"].append("HUGGINGFACE_TOKEN (optional for public models)")
        
        validation_results["all_required_present"] = bool(cls.GEMINI_API_KEY)
        
        return validation_results
    
    @classmethod
    def get_huggingface_auth_kwargs(cls) -> dict:
        """
        Get authentication kwargs for Hugging Face model loading.
        
        Returns:
            dict: Kwargs to pass to Hugging Face model loading functions
        """
        if cls.HUGGINGFACE_TOKEN:
            return {
                "use_auth_token": cls.HUGGINGFACE_TOKEN,
                "token": cls.HUGGINGFACE_TOKEN  # For newer transformers versions
            }
        return {}

# For backward compatibility with legacy code
Config = VideoGenConfig
