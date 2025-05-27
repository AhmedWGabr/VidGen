"""
Tests for file manager utilities
"""

import os
import pytest
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.vidgen.utils.file_manager import (
    get_temp_dir, 
    get_output_dir,
    generate_unique_filename,
    register_temp_file,
    cleanup_temp_files
)

def test_get_temp_dir(monkeypatch):
    """Test getting temporary directory"""
    # Mock os.makedirs
    mock_makedirs = MagicMock()
    monkeypatch.setattr(os, 'makedirs', mock_makedirs)
    
    # Mock os.path.join
    monkeypatch.setattr(os.path, 'join', lambda *args: f"{args[0]}/{args[1]}")
    
    # Set VideoGenConfig mock
    from src.vidgen.core.config import VideoGenConfig
    VideoGenConfig.OUTPUT_DIR = "test_outputs"
    VideoGenConfig.TEMP_DIR = "test_temp"
    
    # Call the function
    result = get_temp_dir()
    
    # Check the result
    assert result == "test_outputs/test_temp"
    mock_makedirs.assert_called_once_with("test_outputs/test_temp", exist_ok=True)

def test_get_output_dir(monkeypatch):
    """Test getting output directory with and without subdir"""
    # Mock os.makedirs
    mock_makedirs = MagicMock()
    monkeypatch.setattr(os, 'makedirs', mock_makedirs)
    
    # Mock os.path.join
    monkeypatch.setattr(os.path, 'join', lambda *args: f"{args[0]}/{args[1]}")
    
    # Set VideoGenConfig mock
    from src.vidgen.core.config import VideoGenConfig
    VideoGenConfig.OUTPUT_DIR = "test_outputs"
    
    # Test without subdir
    result = get_output_dir()
    assert result == "test_outputs"
    mock_makedirs.assert_called_with("test_outputs", exist_ok=True)
    
    # Test with subdir
    result = get_output_dir("videos")
    assert result == "test_outputs/videos"
    mock_makedirs.assert_called_with("test_outputs/videos", exist_ok=True)

def test_generate_unique_filename():
    """Test generating unique filenames"""
    # Generate multiple filenames
    filename1 = generate_unique_filename(prefix="test_", suffix=".txt", directory="temp")
    filename2 = generate_unique_filename(prefix="test_", suffix=".txt", directory="temp")
    
    # They should be different
    assert filename1 != filename2
    
    # Check prefix and suffix
    assert filename1.startswith("temp/test_")
    assert filename1.endswith(".txt")
    
    # Test with default directory (requires mocking get_temp_dir)
    with patch('src.vidgen.utils.file_manager.get_temp_dir', return_value="default_temp"):
        filename = generate_unique_filename(prefix="def_", suffix=".log")
        assert filename.startswith("default_temp/def_")
        assert filename.endswith(".log")

def test_register_temp_file():
    """Test registering temporary files for cleanup"""
    # Reset the _temp_files list
    from src.vidgen.utils.file_manager import _temp_files
    original_temp_files = _temp_files.copy()
    _temp_files.clear()
    
    try:
        # Register some files
        file1 = register_temp_file("/tmp/test1.txt")
        file2 = register_temp_file("/tmp/test2.txt")
        
        # Check that they were added to _temp_files
        from src.vidgen.utils.file_manager import _temp_files
        assert "/tmp/test1.txt" in _temp_files
        assert "/tmp/test2.txt" in _temp_files
        
        # Check that register_temp_file returns the file path
        assert file1 == "/tmp/test1.txt"
        assert file2 == "/tmp/test2.txt"
    finally:
        # Restore original _temp_files
        _temp_files.clear()
        _temp_files.extend(original_temp_files)

def test_cleanup_temp_files(monkeypatch):
    """Test cleaning up temporary files"""
    # Mock os.path.exists and os.remove
    mock_exists = MagicMock(return_value=True)
    mock_remove = MagicMock()
    monkeypatch.setattr(os.path, 'exists', mock_exists)
    monkeypatch.setattr(os, 'remove', mock_remove)
    
    # Reset the _temp_files list
    from src.vidgen.utils.file_manager import _temp_files
    original_temp_files = _temp_files.copy()
    _temp_files.clear()
    
    try:
        # Add some files
        _temp_files.extend(["/tmp/test1.txt", "/tmp/test2.txt"])
        
        # Call cleanup
        cleanup_temp_files()
        
        # Check that os.remove was called for both files
        assert mock_remove.call_count == 2
        mock_remove.assert_any_call("/tmp/test1.txt")
        mock_remove.assert_any_call("/tmp/test2.txt")
    finally:
        # Restore original _temp_files
        _temp_files.clear()
        _temp_files.extend(original_temp_files)

def test_cleanup_temp_files_error_handling(monkeypatch):
    """Test error handling during cleanup"""
    # Mock os.path.exists to return True
    monkeypatch.setattr(os.path, 'exists', MagicMock(return_value=True))
    
    # Mock os.remove to raise an exception
    mock_remove = MagicMock(side_effect=OSError("Test error"))
    monkeypatch.setattr(os, 'remove', mock_remove)
    
    # Reset the _temp_files list
    from src.vidgen.utils.file_manager import _temp_files
    original_temp_files = _temp_files.copy()
    _temp_files.clear()
    
    try:
        # Add a file
        _temp_files.append("/tmp/error_file.txt")
        
        # Call cleanup - should not raise an exception
        cleanup_temp_files()
        
        # Check that os.remove was called
        mock_remove.assert_called_once_with("/tmp/error_file.txt")
    finally:
        # Restore original _temp_files
        _temp_files.clear()
        _temp_files.extend(original_temp_files)

def test_integration_actual_files(temp_dir):
    """Integration test using actual file operations"""
    # Create a real temporary file
    temp_file_path = os.path.join(temp_dir, "real_temp_file.txt")
    with open(temp_file_path, "w") as f:
        f.write("Test content")
    
    # Register it for cleanup
    register_temp_file(temp_file_path)
    
    # Verify file exists
    assert os.path.exists(temp_file_path)
    
    # Clean up
    cleanup_temp_files()
    
    # Verify it was removed
    assert not os.path.exists(temp_file_path)
