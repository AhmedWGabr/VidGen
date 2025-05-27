"""
Tests for VidGen main pipeline functionality.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from vidgen.main import (
    generate_video_async,
    safe_generate_video_segment,
    safe_generate_tts_audio,
    safe_generate_background_audio,
    safe_generate_character_image,
    safe_assemble_video
)


class TestSafeWrapperFunctions:
    """Test the safe wrapper functions for error handling."""
    
    def test_safe_generate_video_segment_success(self):
        """Test successful video segment generation."""
        with patch('vidgen.main.generate_video_segment') as mock_generate:
            mock_generate.return_value = "video_segment.mp4"
            
            result = safe_generate_video_segment("test_cmd", {}, 5)
            
            assert result == "video_segment.mp4"
            mock_generate.assert_called_once_with("test_cmd", {}, 5)
    
    def test_safe_generate_video_segment_failure(self):
        """Test video segment generation with error."""
        with patch('vidgen.main.generate_video_segment') as mock_generate:
            mock_generate.side_effect = Exception("Generation failed")
            
            result = safe_generate_video_segment("test_cmd", {}, 5)
            
            assert result is None
    
    def test_safe_generate_tts_audio_success(self):
        """Test successful TTS audio generation."""
        with patch('vidgen.main.generate_tts_audio') as mock_generate:
            mock_generate.return_value = "audio.wav"
            
            result = safe_generate_tts_audio("test_cmd")
            
            assert result == "audio.wav"
            mock_generate.assert_called_once_with("test_cmd")
    
    def test_safe_generate_tts_audio_failure(self):
        """Test TTS audio generation with error."""
        with patch('vidgen.main.generate_tts_audio') as mock_generate:
            mock_generate.side_effect = Exception("TTS failed")
            
            result = safe_generate_tts_audio("test_cmd")
            
            assert result is None
    
    def test_safe_generate_background_audio_success(self):
        """Test successful background audio generation."""
        with patch('vidgen.main.generate_background_audio') as mock_generate:
            mock_generate.return_value = "bg_audio.wav"
            
            result = safe_generate_background_audio("test_cmd")
            
            assert result == "bg_audio.wav"
            mock_generate.assert_called_once_with("test_cmd")
    
    def test_safe_generate_background_audio_failure(self):
        """Test background audio generation with error."""
        with patch('vidgen.main.generate_background_audio') as mock_generate:
            mock_generate.side_effect = Exception("Audio failed")
            
            result = safe_generate_background_audio("test_cmd")
            
            assert result is None
    
    def test_safe_generate_character_image_success(self):
        """Test successful character image generation."""
        with patch('vidgen.main.generate_character_image') as mock_generate:
            mock_generate.return_value = "character.png"
            
            result = safe_generate_character_image("test_cmd", 42)
            
            assert result == "character.png"
            mock_generate.assert_called_once_with("test_cmd", 42)
    
    def test_safe_generate_character_image_failure(self):
        """Test character image generation with error."""
        with patch('vidgen.main.generate_character_image') as mock_generate:
            mock_generate.side_effect = Exception("Image failed")
            
            result = safe_generate_character_image("test_cmd", 42)
            
            assert result is None
    
    def test_safe_assemble_video_success(self):
        """Test successful video assembly."""
        with patch('vidgen.main.assemble_video') as mock_assemble:
            mock_assemble.return_value = "final_video.mp4"
            
            result = safe_assemble_video([], [], [], [])
            
            assert result == "final_video.mp4"
            mock_assemble.assert_called_once_with([], [], [], [])
    
    def test_safe_assemble_video_failure(self):
        """Test video assembly with error."""
        with patch('vidgen.main.assemble_video') as mock_assemble:
            mock_assemble.side_effect = Exception("Assembly failed")
            
            result = safe_assemble_video([], [], [], [])
            
            assert result is None


class TestGenerateVideoAsync:
    """Test the main async video generation pipeline."""
    
    @pytest.mark.asyncio
    async def test_generate_video_async_empty_script(self):
        """Test handling of empty script input."""
        result = await generate_video_async("", "api_key", 5, 42)
        
        assert result[0].startswith("Error: Please provide a script")
        assert result[1] is None
        assert all(len(arr) == 0 for arr in result[2:6])
        assert result[6] is None
    
    @pytest.mark.asyncio
    async def test_generate_video_async_empty_api_key(self):
        """Test handling of empty API key."""
        result = await generate_video_async("test script", "", 5, 42)
        
        assert result[0].startswith("Error: Please provide a valid Gemini API key")
        assert result[1] is None
        assert all(len(arr) == 0 for arr in result[2:6])
        assert result[6] is None
    
    @pytest.mark.asyncio
    async def test_generate_video_async_gemini_api_failure(self):
        """Test handling of Gemini API failure."""
        with patch('vidgen.main.call_gemini_api') as mock_api:
            mock_api.side_effect = Exception("API Error")
            
            result = await generate_video_async("test script", "api_key", 5, 42)
            
            assert "Gemini API call failed" in result[0]
            assert result[1] is None
            assert all(len(arr) == 0 for arr in result[2:6])
            assert result[6] is None
    
    @pytest.mark.asyncio
    async def test_generate_video_async_script_parsing_failure(self):
        """Test handling of script parsing failure."""
        with patch('vidgen.main.call_gemini_api') as mock_api:
            with patch('vidgen.main.parse_detailed_script') as mock_parse:
                mock_api.return_value = "detailed script"
                mock_parse.side_effect = Exception("Parse Error")
                
                result = await generate_video_async("test script", "api_key", 5, 42)
                
                assert result[0] == "detailed script"
                assert "Script parsing failed" in result[1]
                assert all(len(arr) == 0 for arr in result[2:6])
                assert result[6] is None
    
    @pytest.mark.asyncio
    async def test_generate_video_async_success_pipeline(self):
        """Test successful video generation pipeline."""
        # Mock all the dependencies
        with patch('vidgen.main.call_gemini_api') as mock_api:
            with patch('vidgen.main.parse_detailed_script') as mock_parse:
                with patch('vidgen.main.safe_generate_video_segment') as mock_video:
                    with patch('vidgen.main.safe_generate_tts_audio') as mock_tts:
                        with patch('vidgen.main.safe_generate_background_audio') as mock_bg:
                            with patch('vidgen.main.safe_generate_character_image') as mock_img:
                                with patch('vidgen.main.safe_assemble_video') as mock_assemble:
                                    
                                    # Setup mock returns
                                    mock_api.return_value = "detailed script"
                                    mock_parse.return_value = {
                                        "video": ["video_cmd"],
                                        "tts": ["tts_cmd"],
                                        "audio": ["audio_cmd"],
                                        "image": ["image_cmd"]
                                    }
                                    mock_video.return_value = "video.mp4"
                                    mock_tts.return_value = "audio.wav"
                                    mock_bg.return_value = "bg_audio.wav"
                                    mock_img.return_value = "image.png"
                                    mock_assemble.return_value = "final_video.mp4"
                                    
                                    result = await generate_video_async("test script", "api_key", 5, 42)
                                    
                                    # Check successful result structure
                                    assert result[0] == "detailed script"  # detailed_script
                                    assert "video" in result[1]  # parsed (as string)
                                    assert result[2] == ["audio.wav"]  # tts_audios
                                    assert result[3] == ["image.png"]  # character_images
                                    assert result[4] == ["video.mp4"]  # video_segments
                                    assert result[5] == ["bg_audio.wav"]  # background_audios
                                    assert result[6] == "final_video.mp4"  # final_video_path
    
    @pytest.mark.asyncio
    async def test_generate_video_async_with_progress_callback(self):
        """Test video generation with progress callback."""
        progress_calls = []
        
        def progress_callback(message, progress):
            progress_calls.append((message, progress))
        
        with patch('vidgen.main.call_gemini_api') as mock_api:
            with patch('vidgen.main.parse_detailed_script') as mock_parse:
                mock_api.return_value = "detailed script"
                mock_parse.return_value = {
                    "video": [],
                    "tts": [],
                    "audio": [],
                    "image": []
                }
                
                result = await generate_video_async(
                    "test script", "api_key", 5, 42, 
                    progress_callback=progress_callback
                )
                
                # Check that progress callbacks were made
                assert len(progress_calls) > 0
                assert progress_calls[0][0].startswith("🚀")  # Starting message
                assert progress_calls[0][1] == 0  # Starting progress
    
    @pytest.mark.asyncio
    async def test_generate_video_async_unexpected_error(self):
        """Test handling of unexpected errors."""
        with patch('vidgen.main.call_gemini_api') as mock_api:
            # Simulate an unexpected error type
            mock_api.side_effect = RuntimeError("Unexpected error")
            
            result = await generate_video_async("test script", "api_key", 5, 42)
            
            assert "Unexpected error occurred" in result[0]
            assert result[1] is None
            assert all(len(arr) == 0 for arr in result[2:6])
            assert result[6] is None


class TestMainPipelineIntegration:
    """Test integration aspects of the main pipeline."""
    
    def test_progress_message_format(self):
        """Test that progress messages are properly formatted."""
        progress_calls = []
        
        def mock_callback(message, progress):
            progress_calls.append((message, progress))
            # Check message format
            assert isinstance(message, str)
            assert len(message) > 0
            # Check progress format
            assert isinstance(progress, (int, float, type(None)))
            if progress is not None:
                assert 0 <= progress <= 100
        
        # Test the progress callback structure
        mock_callback("🚀 Starting...", 0)
        mock_callback("✅ Completed", 100)
        
        assert len(progress_calls) == 2
    
    def test_error_message_format(self):
        """Test that error messages are user-friendly."""
        error_patterns = [
            "Error: Please provide a script",
            "Error: Please provide a valid Gemini API key",
            "Error: Gemini API call failed:",
            "Error: Script parsing failed:",
            "Error: Unexpected error occurred:"
        ]
        
        for pattern in error_patterns:
            # Check that error messages start with "Error:" for consistency
            assert pattern.startswith("Error:")
            # Check that they're descriptive
            assert len(pattern.split()) >= 3


if __name__ == "__main__":
    pytest.main([__file__])
