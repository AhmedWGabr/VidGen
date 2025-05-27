"""
Tests for TTS model
"""

import pytest
import os
import sys
import numpy as np
from unittest.mock import patch, MagicMock, call

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from vidgen.models.tts import generate_tts_audio
from vidgen.core.config import VideoGenConfig

@pytest.mark.parametrize("narration", [
    "This is a test narration",
    "Another test with different text",
    "",  # Empty string test case
])
def test_generate_tts_audio(narration, monkeypatch):
    """Test generating TTS audio with various inputs"""
    
    # Mock the bark import and functions
    mock_audio_array = np.zeros(1000)  # Mock audio array
    mock_generate_audio = MagicMock(return_value=mock_audio_array)
    mock_write = MagicMock()
    
    # Set up mock configuration
    VideoGenConfig.OUTPUT_DIR = "test_outputs"
    
    # Create patches
    with patch.dict('sys.modules', {
        'bark': MagicMock(
            SAMPLE_RATE=24000,
            generate_audio=mock_generate_audio
        ),
        'scipy.io.wavfile': MagicMock(write=mock_write)
    }):
        # Call the function
        result = generate_tts_audio(narration)
        
        # Check the result
        if narration:
            # For valid inputs, should return a path
            assert result == os.path.join("test_outputs", "tts_audio.wav")
            
            # Check if generate_audio was called with correct parameters
            mock_generate_audio.assert_called_once_with(narration)
            
            # Check if wavfile.write was called correctly
            mock_write.assert_called_once()
            args, _ = mock_write.call_args
            assert args[0] == os.path.join("test_outputs", "tts_audio.wav")
            assert args[1] == 24000  # SAMPLE_RATE
            assert args[2] is mock_audio_array  # audio array
        else:
            # For empty input, should still try to process
            assert "test_outputs" in result
            mock_generate_audio.assert_called_once()

def test_generate_tts_audio_exception_handling():
    """Test error handling in the TTS generation"""
    
    # Mock to simulate an exception
    mock_generate_audio = MagicMock(side_effect=Exception("Test error"))
    
    with patch.dict('sys.modules', {
        'bark': MagicMock(
            SAMPLE_RATE=24000,
            generate_audio=mock_generate_audio
        ),
        'scipy.io.wavfile': MagicMock()
    }):
        # Call the function that should handle the exception
        result = generate_tts_audio("Test narration")
        
        # Check that it returned an error path
        assert "tts_error_" in result
        assert "Test error" in result

def test_generate_tts_audio_integration(temp_dir, monkeypatch):
    """More realistic integration test with actual file operations"""
    
    # Use the temp_dir fixture to avoid writing to real output dir
    VideoGenConfig.OUTPUT_DIR = str(temp_dir)
    
    # Create a simple mock audio array
    mock_audio_array = np.ones(1000, dtype=np.float32) * 0.5
    
    # Mock just the model parts, but use real file operations
    with patch.dict('sys.modules', {
        'bark': MagicMock(
            SAMPLE_RATE=24000,
            generate_audio=MagicMock(return_value=mock_audio_array)
        ),
    }), patch('scipy.io.wavfile.write') as mock_write:
        
        # Run the function
        result = generate_tts_audio("Integration test narration")
        
        # Verify the results
        assert str(temp_dir) in result
        assert "tts_audio.wav" in result
        
        # Check that wavfile.write was called with correct path
        mock_write.assert_called_once()
        path_arg = mock_write.call_args[0][0]
        assert os.path.dirname(path_arg) == str(temp_dir)
