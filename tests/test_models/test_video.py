# Test for video model

"""
Tests for video generation module
"""

import os
import pytest
from unittest.mock import patch, MagicMock, call
from src.vidgen.models.video import generate_video_segment
from src.vidgen.core.config import VideoGenConfig

@pytest.fixture
def mock_subprocess():
    """Mock subprocess for testing"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        yield mock_run

@pytest.fixture
def video_command():
    """Sample video command for testing"""
    return {
        "start": 0,
        "end": 5,
        "narration": "This is a test narration",
        "scene": "A test scene with mountains",
        "character_face": {
            "character": "Narrator",
            "face_prompt": "Narrator: Professional with glasses",
            "seed": 42
        }
    }

def test_generate_video_segment_basic(video_command, mock_subprocess, monkeypatch):
    """Test basic video segment generation"""
    # Mock dependencies
    mock_generate_character_image = MagicMock(return_value="/path/to/image.png")
    mock_generate_tts_audio = MagicMock(return_value="/path/to/audio.wav")
    
    monkeypatch.setattr('src.vidgen.models.video.generate_character_image', mock_generate_character_image)
    monkeypatch.setattr('src.vidgen.models.video.generate_tts_audio', mock_generate_tts_audio)
    
    # Set configuration
    VideoGenConfig.OUTPUT_DIR = "test_outputs"
    
    # Call the function
    with patch('uuid.uuid4', return_value=MagicMock(hex='test123')):
        result = generate_video_segment(video_command)
    
    # Check that the dependencies were called correctly
    mock_generate_character_image.assert_called_once_with(
        "Narrator: Professional with glasses", 
        seed=42
    )
    
    mock_generate_tts_audio.assert_called_once_with("This is a test narration")
    
    # Check that ffmpeg was called with the right parameters
    mock_subprocess.assert_called_once()
    ffmpeg_call = mock_subprocess.call_args[0][0]
    
    # Verify key parts of the ffmpeg command
    assert ffmpeg_call[0] == "ffmpeg"
    assert "-i" in ffmpeg_call
    assert "/path/to/image.png" in ffmpeg_call
    assert "/path/to/audio.wav" in ffmpeg_call
    assert "-t" in ffmpeg_call
    assert "5" in ffmpeg_call  # Duration from end-start
    
    # Verify the output path
    expected_output = os.path.join("test_outputs", "video_segment_test123.mp4")
    assert expected_output in ffmpeg_call
    assert result == expected_output

def test_generate_video_segment_with_face_cache(video_command, mock_subprocess, monkeypatch):
    """Test video generation with face cache for character consistency"""
    # Mock dependencies
    mock_generate_character_image = MagicMock(return_value="/path/to/new_image.png")
    mock_generate_tts_audio = MagicMock(return_value="/path/to/audio.wav")
    
    monkeypatch.setattr('src.vidgen.models.video.generate_character_image', mock_generate_character_image)
    monkeypatch.setattr('src.vidgen.models.video.generate_tts_audio', mock_generate_tts_audio)
    
    # Create a face cache with existing entry
    face_cache = {
        ("Narrator", 42): "/path/to/cached_image.png"
    }
    
    # Call the function with the face cache
    with patch('uuid.uuid4', return_value=MagicMock(hex='test456')):
        result = generate_video_segment(video_command, face_cache=face_cache)
    
    # Check that the character image was not regenerated (used cache)
    mock_generate_character_image.assert_not_called()
    
    # Verify the cached image was used in the ffmpeg command
    ffmpeg_call = mock_subprocess.call_args[0][0]
    assert "/path/to/cached_image.png" in ffmpeg_call

def test_generate_video_segment_adds_to_cache(video_command, mock_subprocess, monkeypatch):
    """Test that generating a video segment adds the character to the face cache"""
    # Mock dependencies
    mock_generate_character_image = MagicMock(return_value="/path/to/new_char.png")
    mock_generate_tts_audio = MagicMock(return_value="/path/to/audio.wav")
    
    monkeypatch.setattr('src.vidgen.models.video.generate_character_image', mock_generate_character_image)
    monkeypatch.setattr('src.vidgen.models.video.generate_tts_audio', mock_generate_tts_audio)
    
    # Empty face cache
    face_cache = {}
    
    # Call the function
    generate_video_segment(video_command, face_cache=face_cache)
    
    # Check that the character was added to the cache
    assert ("Narrator", 42) in face_cache
    assert face_cache[("Narrator", 42)] == "/path/to/new_char.png"

def test_generate_video_segment_default_duration(mock_subprocess, monkeypatch):
    """Test video generation with default duration when not specified"""
    # Create a command without duration
    command_without_duration = {
        "narration": "Test narration",
        "character_face": {
            "character": "Test",
            "face_prompt": "Test character",
            "seed": 100
        }
    }
    
    # Mock dependencies
    mock_generate_character_image = MagicMock(return_value="/path/to/image.png")
    mock_generate_tts_audio = MagicMock(return_value="/path/to/audio.wav")
    
    monkeypatch.setattr('src.vidgen.models.video.generate_character_image', mock_generate_character_image)
    monkeypatch.setattr('src.vidgen.models.video.generate_tts_audio', mock_generate_tts_audio)
    
    # Call the function with a custom default duration
    default_duration = 10
    generate_video_segment(command_without_duration, default_duration=default_duration)
    
    # Verify the duration in the ffmpeg command
    ffmpeg_call = mock_subprocess.call_args[0][0]
    duration_index = ffmpeg_call.index("-t") + 1
    assert ffmpeg_call[duration_index] == str(default_duration)

def test_generate_video_segment_error_handling(monkeypatch):
    """Test error handling in video generation"""
    # Mock subprocess to raise an exception
    mock_subprocess_run = MagicMock(side_effect=Exception("FFmpeg error"))
    monkeypatch.setattr('subprocess.run', mock_subprocess_run)
    
    # Mock other dependencies to avoid their errors
    monkeypatch.setattr('src.vidgen.models.video.generate_character_image', 
                       MagicMock(return_value="/path/to/image.png"))
    monkeypatch.setattr('src.vidgen.models.video.generate_tts_audio', 
                       MagicMock(return_value="/path/to/audio.wav"))
    
    # Test with a simple command
    command = {
        "start": 0,
        "end": 5,
        "narration": "Test"
    }
    
    # The function should raise the exception
    with pytest.raises(Exception, match="FFmpeg error"):
        generate_video_segment(command)

def test_generate_video_segment_integration(mock_subprocess, mock_video_config, temp_dir):
    """More realistic integration test"""
    # Set up configuration to use the temp directory
    mock_video_config.OUTPUT_DIR = str(temp_dir)
    
    # Create a test command
    command = {
        "start": 0, 
        "end": 5,
        "narration": "Integration test narration",
        "scene": "Test scene description"
    }
    
    # Set up the mocks but with more realistic paths
    with patch('src.vidgen.models.video.generate_character_image', 
               return_value=os.path.join(temp_dir, "test_image.png")), \
         patch('src.vidgen.models.video.generate_tts_audio',
               return_value=os.path.join(temp_dir, "test_audio.wav")), \
         patch('uuid.uuid4', return_value=MagicMock(hex='integration123')):
        
        # Actually create the test files to ensure paths exist
        with open(os.path.join(temp_dir, "test_image.png"), 'w') as f:
            f.write("mock image data")
        with open(os.path.join(temp_dir, "test_audio.wav"), 'w') as f:
            f.write("mock audio data")
        
        # Call the function
        result = generate_video_segment(command)
        
        # Expected output path
        expected_path = os.path.join(str(temp_dir), "video_segment_integration123.mp4")
        
        # Check the result
        assert result == expected_path
        
        # Verify ffmpeg was called with proper paths
        ffmpeg_call = mock_subprocess.call_args[0][0]
        assert os.path.join(temp_dir, "test_image.png") in ffmpeg_call
        assert os.path.join(temp_dir, "test_audio.wav") in ffmpeg_call
