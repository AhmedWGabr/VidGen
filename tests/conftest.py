"""
Pytest configuration and fixtures for VidGen tests
"""

import os
import sys
import json
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_script():
    """Sample script for testing"""
    return """
    Scene 1: A beautiful sunset over the ocean
    Character: Narrator
    Dialogue: The day comes to an end as the sun sets over the horizon.
    
    Scene 2: A busy city street
    Character: Reporter
    Dialogue: Meanwhile, in the city, life continues at its usual pace.
    """

@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    return {
        "output_dir": "test_outputs",
        "temp_dir": "test_temp",
        "models": {
            "tts": "test_tts_model",
            "image": "test_image_model"
        }
    }

@pytest.fixture
def detailed_script_json():
    """Detailed script JSON for testing"""
    return json.dumps([
        {
            "start": 0,
            "end": 5,
            "scene": "A sunset over the ocean",
            "narration": "The day comes to an end",
            "audio": "Soft piano music",
            "visual": "Wide shot of ocean horizon",
            "image": "Sunset: Orange and red sky over calm water"
        },
        {
            "start": 5,
            "end": 10,
            "scene": "A busy city street",
            "narration": "Meanwhile, in the city, life continues",
            "audio": "Urban ambient sounds",
            "visual": "Panning shot of city street",
            "image": "City: Modern buildings and busy streets"
        }
    ])

@pytest.fixture
def mock_image_pipeline():
    """Mock Stable Diffusion pipeline for testing"""
    mock_pipeline = MagicMock()
    mock_images = MagicMock()
    mock_images.__getitem__.return_value = MagicMock()
    mock_pipeline.return_value.images = mock_images
    
    with patch.dict('sys.modules', {
        'diffusers': MagicMock(StableDiffusionPipeline=mock_pipeline),
        'torch': MagicMock(
            float16='float16',
            cuda=MagicMock(is_available=MagicMock(return_value=True)),
            Generator=MagicMock(return_value=MagicMock(manual_seed=MagicMock(return_value="mock_generator")))
        )
    }):
        yield mock_pipeline

@pytest.fixture
def mock_tts():
    """Mock TTS model for testing"""
    mock_generate_audio = MagicMock(return_value="mock_audio_array")
    mock_write = MagicMock()
    
    with patch.dict('sys.modules', {
        'bark': MagicMock(
            SAMPLE_RATE=24000,
            generate_audio=mock_generate_audio
        ),
        'scipy.io.wavfile': MagicMock(write=mock_write)
    }):
        yield mock_generate_audio, mock_write

@pytest.fixture
def mock_ffmpeg():
    """Mock FFmpeg for testing video assembly"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        yield mock_run

@pytest.fixture
def sample_character():
    """Sample character data for testing"""
    from src.vidgen.models.data_models import Character
    return Character(
        name="Narrator",
        description="Professional narrator with deep voice",
        seed=12345
    )

@pytest.fixture
def sample_script_segment():
    """Sample script segment for testing"""
    from src.vidgen.models.data_models import ScriptSegment, Character
    
    character = Character(
        name="Narrator",
        description="Professional narrator with deep voice",
        seed=12345
    )
    
    return ScriptSegment(
        timestamp=0.0,
        duration=5.0,
        narration="This is a test narration for the video",
        character=character,
        scene_description="A beautiful sunset over the ocean"
    )

@pytest.fixture
def mock_video_config():
    """Mock the VideoGenConfig class for testing"""
    with patch('src.vidgen.core.config.VideoGenConfig') as mock_config:
        mock_config.OUTPUT_DIR = "test_outputs"
        mock_config.TEMP_DIR = "test_temp"
        mock_config.STABLE_DIFFUSION_MODEL = "test_model"
        mock_config.DEFAULT_SEGMENT_DURATION = 5
        yield mock_config

@pytest.fixture
def mock_gemini_api():
    """Mock the Gemini API call"""
    with patch('src.vidgen.services.gemini_api.call_gemini_api') as mock_api:
        mock_api.return_value = json.dumps([
            {
                "start": 0,
                "end": 5,
                "scene": "A test scene",
                "narration": "Test narration",
                "audio": "Test audio",
                "image": "Test character"
            }
        ])
        yield mock_api

@pytest.fixture
def mock_logger():
    """Mock logger for testing"""
    with patch('logging.getLogger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        yield mock_logger
