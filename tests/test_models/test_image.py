# Test for image model

"""
Tests for the image generation module
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock, PropertyMock

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from vidgen.models.image import generate_character_image, get_image_pipeline
from vidgen.core.config import VideoGenConfig

@pytest.fixture
def mock_diffusers():
    """Mock for the diffusers module"""
    mock_pipeline = MagicMock()
    mock_images = PropertyMock(return_value=[MagicMock()])
    type(mock_pipeline.return_value).images = mock_images
    
    with patch.dict('sys.modules', {
        'diffusers': MagicMock(StableDiffusionPipeline=mock_pipeline),
        'torch': MagicMock(
            float16='float16',
            cuda=MagicMock(is_available=MagicMock(return_value=True)),
            Generator=MagicMock(return_value=MagicMock(manual_seed=MagicMock(return_value=MagicMock())))
        )
    }):
        yield mock_pipeline

def test_get_image_pipeline(mock_diffusers):
    """Test getting and caching the image generation pipeline"""
    # Reset global _image_pipeline to ensure test isolation
    import vidgen.models.image
    original_pipeline = vidgen.models.image._image_pipeline
    vidgen.models.image._image_pipeline = None
    
    try:
        # Set model configuration
        VideoGenConfig.STABLE_DIFFUSION_MODEL = "test/stable-diffusion-v1-5"
        
        # Call the function
        pipeline1 = get_image_pipeline()
        
        # Check it was initialized
        mock_diffusers.assert_called_once_with(
            "test/stable-diffusion-v1-5",
            torch_dtype='float16'
        )
        
        # Call again to test caching
        pipeline2 = get_image_pipeline()
        
        # Check it was not initialized again (still just one call)
        mock_diffusers.assert_called_once()
          # Both calls should return the same object
        assert pipeline1 is pipeline2
    finally:
        # Restore original _image_pipeline
        vidgen.models.image._image_pipeline = original_pipeline

def test_generate_character_image(mock_diffusers, monkeypatch):
    """Test character image generation"""
    # Set up configuration
    VideoGenConfig.OUTPUT_DIR = "/test/output"
    
    # Mock image.save
    mock_save = MagicMock()
    monkeypatch.setattr(mock_diffusers.return_value.images[0], 'save', mock_save)
    
    # Mock os.path.join
    monkeypatch.setattr(os.path, 'join', lambda *args: f"{args[0]}/{args[1]}")
    
    # Call the function
    prompt = "A beautiful mountain landscape"
    result = generate_character_image(prompt, seed=123)
    
    # Check the result
    assert result == "/test/output/character_image.png"
    
    # Check that the pipeline was called with the prompt
    mock_diffusers.return_value.assert_called_once()
    assert mock_diffusers.return_value.call_args[0][0] == prompt
    
    # Check that the image was saved
    mock_save.assert_called_once_with("/test/output/character_image.png")

def test_generate_character_image_error_handling(monkeypatch):
    """Test error handling during image generation"""
    # Mock get_image_pipeline to raise an exception
    monkeypatch.setattr('vidgen.models.image.get_image_pipeline', 
                        MagicMock(side_effect=Exception("Test error")))
    
    # Call the function
    result = generate_character_image("Test prompt")
    
    # Should return the placeholder image path
    assert result == "placeholder_image.png"

def test_generate_character_image_with_seed():
    """Test that seed affects the image generation"""
    # We'll mock the torch generator and verify the seed is used
    with patch.dict('sys.modules', {
        'torch': MagicMock(
            cuda=MagicMock(is_available=MagicMock(return_value=True)),
            Generator=MagicMock(return_value=MagicMock(manual_seed=MagicMock()))
        )
    }),        patch('vidgen.models.image.get_image_pipeline') as mock_get_pipeline, \
        patch('vidgen.models.image.os.path.join', return_value="test_path.png"), \
        patch('vidgen.models.image.logging'):
        
        # Set up a mock pipeline that returns a mock image
        mock_image = MagicMock()
        mock_image.save = MagicMock()
        mock_pipeline = MagicMock()
        mock_pipeline.return_value.images = [mock_image]
        mock_get_pipeline.return_value = mock_pipeline
        
        # Call with different seeds
        generate_character_image("Test prompt", seed=123)
        generate_character_image("Test prompt", seed=456)
        
        # Get the generator calls
        import torch
        generator_calls = torch.Generator.return_value.manual_seed.call_args_list
        
        # Verify different seeds were used
        assert generator_calls[0][0][0] == 123
        assert generator_calls[1][0][0] == 456
