# Test for video assembler service
"""
Tests for video assembler service
"""

import pytest
import os
from unittest.mock import patch, MagicMock, call
import subprocess
from src.vidgen.services.video_assembler import assemble_video, cleanup_temp_files
from src.vidgen.core.config import VideoGenConfig

@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run to avoid actual command execution"""
    with patch('subprocess.run') as mock_run:
        yield mock_run

@pytest.fixture
def mock_file_operations():
    """Mock file operations"""
    with patch('builtins.open', MagicMock()), \
         patch('os.path.join', lambda *args: '/'.join(args)), \
         patch('shutil.copy2') as mock_copy:
        yield mock_copy

@pytest.fixture
def test_files():
    """Test file paths"""
    return {
        'video_segments': ['segment1.mp4', 'segment2.mp4'],
        'tts_audios': ['speech1.wav', 'speech2.wav'],
        'background_audios': ['music1.wav', 'music2.wav'],
        'character_images': ['character1.png', 'character2.png'],
        'output_path': 'final_video.mp4'
    }

def test_assemble_video_no_segments():
    """Test assembling with no video segments"""
    # Call with empty segments list
    result = assemble_video([], [], [], [])
    
    # Should return default error video path
    assert result == "no_video_segments.mp4"

def test_assemble_video_default_output_path(mock_file_operations):
    """Test assembling with default output path"""
    # Set configuration
    VideoGenConfig.OUTPUT_DIR = "/test/output"
    
    with patch('subprocess.run'):
        # Call with no output path
        result = assemble_video(['segment.mp4'], [], [], [])
        
        # Should use default output path
        assert result == "/test/output/final_video.mp4"

def test_assemble_video_with_video_only(mock_subprocess_run, mock_file_operations, test_files):
    """Test assembling with only video segments"""
    # Call with video segments only
    result = assemble_video(
        test_files['video_segments'], 
        [], 
        [], 
        [], 
        test_files['output_path']
    )
    
    # Check subprocess calls
    assert mock_subprocess_run.call_count >= 1
    # First call should be ffmpeg concat for video segments
    first_call_args = mock_subprocess_run.call_args_list[0][0][0]
    assert "ffmpeg" in first_call_args
    assert "concat" in first_call_args
    
    # Should return the output path
    assert result == test_files['output_path']

def test_assemble_video_with_audio(mock_subprocess_run, mock_file_operations, test_files):
    """Test assembling with video and audio"""
    # Call with video and audio
    result = assemble_video(
        test_files['video_segments'], 
        test_files['tts_audios'], 
        [], 
        [], 
        test_files['output_path']
    )
    
    # Check subprocess calls
    assert mock_subprocess_run.call_count >= 2
    # Last call should include audio
    last_call_args = mock_subprocess_run.call_args_list[-1][0][0]
    assert "ffmpeg" in last_call_args
    assert "-i" in last_call_args
    assert "final_audio.wav" in " ".join(last_call_args)
    
    # Should return the output path
    assert result == test_files['output_path']

def test_assemble_video_with_mixed_audio(mock_subprocess_run, mock_file_operations, test_files):
    """Test assembling with mixed audio (TTS + background)"""
    # Call with video, TTS, and background audio
    result = assemble_video(
        test_files['video_segments'], 
        test_files['tts_audios'], 
        test_files['background_audios'], 
        [], 
        test_files['output_path']
    )
    
    # Check subprocess calls
    # Should have at least 3 calls: concat video, mix audio, final assembly
    assert mock_subprocess_run.call_count >= 3
    
    # Check for audio mixing in the calls (amix filter)
    mix_calls = [call for call in mock_subprocess_run.call_args_list 
                 if any("amix" in str(arg) for arg in call[0][0])]
    assert len(mix_calls) > 0
    
    # Should return the output path
    assert result == test_files['output_path']

def test_assemble_video_with_character_images(mock_subprocess_run, mock_file_operations, test_files):
    """Test assembling with character images overlay"""
    # Call with video and character images
    result = assemble_video(
        test_files['video_segments'], 
        [], 
        [], 
        test_files['character_images'], 
        test_files['output_path']
    )
    
    # Check for overlay command in subprocess calls
    overlay_calls = [call for call in mock_subprocess_run.call_args_list 
                     if any("overlay" in str(arg) for arg in call[0][0])]
    assert len(overlay_calls) > 0
    
    # Should return the output path
    assert result == test_files['output_path']

def test_assemble_video_error_handling(mock_subprocess_run):
    """Test error handling during assembly"""
    # Make subprocess.run raise an exception
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "ffmpeg")
    
    # Call should handle the error
    result = assemble_video(['segment.mp4'], [], [], [], 'output.mp4')
    
    # Should return None on error
    assert result is None

def test_cleanup_temp_files(mock_subprocess_run):
    """Test cleanup of temporary files"""
    # Set up configuration
    VideoGenConfig.TEMP_DIR = "/test/temp"
    
    # Call cleanup
    cleanup_temp_files()
    
    # Check if subprocess was called with rm command
    mock_subprocess_run.assert_called_once()
    cmd_args = mock_subprocess_run.call_args[0][0]
    assert "rm" in cmd_args
    assert "/test/temp/*" in " ".join(cmd_args)
