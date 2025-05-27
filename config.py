import os

class Config:
    # Model settings
    STABLE_DIFFUSION_MODEL = "runwayml/stable-diffusion-v1-5"
    DEFAULT_SEGMENT_DURATION = 5

    # Paths
    OUTPUT_DIR = "outputs"
    TEMP_DIR = "temp"

    # API settings
    GEMINI_MODEL = "gemini-2.0-flash-001"

    @classmethod
    def ensure_dirs(cls):
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
