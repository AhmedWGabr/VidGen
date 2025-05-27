"""
Tests for VidGen core configuration functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from vidgen.core.config import VideoGenConfig


class TestVideoGenConfig:
    """Test VideoGenConfig functionality."""
    
    def test_config_initialization(self):
        """Test that config initializes with default values."""
        config = VideoGenConfig()
        
        # Test default paths exist
        assert hasattr(config, 'OUTPUT_DIR')
        assert hasattr(config, 'TEMP_DIR')
        assert hasattr(config, 'MODELS_DIR')
        
        # Test directories are Path objects
        assert isinstance(config.OUTPUT_DIR, Path)
        assert isinstance(config.TEMP_DIR, Path)
        assert isinstance(config.MODELS_DIR, Path)
    
    def test_ensure_dirs_creates_directories(self):
        """Test that ensure_dirs creates necessary directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock the config directories to use temp directory
            with patch.object(VideoGenConfig, 'OUTPUT_DIR', Path(temp_dir) / 'output'):
                with patch.object(VideoGenConfig, 'TEMP_DIR', Path(temp_dir) / 'temp'):
                    with patch.object(VideoGenConfig, 'MODELS_DIR', Path(temp_dir) / 'models'):
                        
                        VideoGenConfig.ensure_dirs()
                        
                        # Check directories were created
                        assert (Path(temp_dir) / 'output').exists()
                        assert (Path(temp_dir) / 'temp').exists()
                        assert (Path(temp_dir) / 'models').exists()
    
    def test_ensure_dirs_handles_existing_directories(self):
        """Test that ensure_dirs works when directories already exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / 'output'
            output_dir.mkdir()
            
            with patch.object(VideoGenConfig, 'OUTPUT_DIR', output_dir):
                with patch.object(VideoGenConfig, 'TEMP_DIR', Path(temp_dir) / 'temp'):
                    with patch.object(VideoGenConfig, 'MODELS_DIR', Path(temp_dir) / 'models'):
                        
                        # Should not raise exception
                        VideoGenConfig.ensure_dirs()
                        assert output_dir.exists()
    
    @patch('vidgen.core.config.logging.basicConfig')
    def test_configure_logging(self, mock_basic_config):
        """Test logging configuration."""
        VideoGenConfig.configure_logging()
        
        # Check that logging.basicConfig was called
        mock_basic_config.assert_called_once()
        
        # Check the call arguments contain expected values
        call_args = mock_basic_config.call_args
        assert 'level' in call_args.kwargs
        assert 'format' in call_args.kwargs
        assert 'handlers' in call_args.kwargs
    
    def test_get_output_path(self):
        """Test getting output path for files."""
        config = VideoGenConfig()
        
        # Test basic filename
        path = config.get_output_path("test.mp4")
        assert path.name == "test.mp4"
        assert path.parent == config.OUTPUT_DIR
        
        # Test with subdirectory
        path = config.get_output_path("videos/test.mp4")
        assert path.name == "test.mp4"
        assert path.parent.name == "videos"
    
    def test_get_temp_path(self):
        """Test getting temporary path for files."""
        config = VideoGenConfig()
        
        path = config.get_temp_path("temp_file.txt")
        assert path.name == "temp_file.txt"
        assert path.parent == config.TEMP_DIR
    
    def test_cleanup_temp_files(self):
        """Test temporary file cleanup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create some test files
            (temp_path / "test1.txt").write_text("test")
            (temp_path / "test2.txt").write_text("test")
            
            with patch.object(VideoGenConfig, 'TEMP_DIR', temp_path):
                config = VideoGenConfig()
                config.cleanup_temp_files()
                
                # Check files were removed
                assert not (temp_path / "test1.txt").exists()
                assert not (temp_path / "test2.txt").exists()
    
    def test_get_model_path(self):
        """Test getting model path."""
        config = VideoGenConfig()
        
        path = config.get_model_path("stable-diffusion")
        assert path.parent == config.MODELS_DIR
        assert "stable-diffusion" in str(path)


class TestVideoGenConfigConstants:
    """Test VideoGenConfig constants and settings."""
    
    def test_model_settings_exist(self):
        """Test that model configuration settings exist."""
        config = VideoGenConfig()
        
        # Check that model-related constants exist
        assert hasattr(config, 'DEFAULT_IMAGE_SIZE')
        assert hasattr(config, 'DEFAULT_AUDIO_DURATION')
        assert hasattr(config, 'DEFAULT_VIDEO_FPS')
    
    def test_api_settings_exist(self):
        """Test that API configuration settings exist."""
        config = VideoGenConfig()
        
        # Check API-related settings
        assert hasattr(config, 'GEMINI_MODEL_NAME')
        assert hasattr(config, 'MAX_RETRY_ATTEMPTS')
    
    def test_file_format_settings(self):
        """Test file format configuration."""
        config = VideoGenConfig()
        
        # Check supported formats are defined
        assert hasattr(config, 'SUPPORTED_IMAGE_FORMATS')
        assert hasattr(config, 'SUPPORTED_AUDIO_FORMATS')
        assert hasattr(config, 'SUPPORTED_VIDEO_FORMATS')
        
        # Verify they are lists/tuples
        assert isinstance(config.SUPPORTED_IMAGE_FORMATS, (list, tuple))
        assert isinstance(config.SUPPORTED_AUDIO_FORMATS, (list, tuple))
        assert isinstance(config.SUPPORTED_VIDEO_FORMATS, (list, tuple))


if __name__ == "__main__":
    pytest.main([__file__])
