import os
import logging

class VideoGenConfig:
    """Centralized configuration with validation and environment support."""
    # Model settings
    STABLE_DIFFUSION_MODEL = "runwayml/stable-diffusion-v1-5"
    DEFAULT_SEGMENT_DURATION = 5

    # Paths
    OUTPUT_DIR = "outputs"
    TEMP_DIR = "temp"

    # API settings
    GEMINI_MODEL = "gemini-2.0-flash-001"
    LOG_LEVEL = logging.INFO

    @classmethod
    def ensure_dirs(cls):
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True)

    @classmethod
    def configure_logging(cls):
        logging.basicConfig(
            level=cls.LOG_LEVEL,
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
        )
