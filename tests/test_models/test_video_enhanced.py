"""
Tests for video generation enhancements
"""
import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock

from vidgen.models.video import (
    generate_video_segment,
    generate_video_with_transitions,
    add_motion_effects,
    create_multi_angle_video,
    concatenate_videos,
    _build_transition_filter,
    _create_zoom_pan_filter,
    _create_parallax_filter,
    _create_shake_filter,
    create_fallback_image,
    create_silent_audio
)
from vidgen.core.exceptions import VideoAssemblyError


class TestVideoGeneration:
    
    @patch('vidgen.models.video.generate_character_image')
    @patch('vidgen.models.video.generate_tts_audio')
    @patch('subprocess.run')
    def test_generate_video_segment_success(self, mock_subprocess, mock_tts, mock_image):
        """Test successful video segment generation"""
        mock_image.return_value = "/path/to/image.png"
        mock_tts.return_value = "/path/to/audio.wav"
        mock_subprocess.return_value = MagicMock()
        
        video_command = {
            "narration": "Hello world",
            "start": 0,
            "end": 5,
            "character_face": {
                "character": "narrator",
                "face_prompt": "friendly person",
                "seed": 42
            }
        }
        
        result = generate_video_segment(video_command)
        assert result is not None
        assert result.endswith('.mp4')
        
        mock_image.assert_called_once()
        mock_tts.assert_called_once_with("Hello world")
        mock_subprocess.assert_called_once()
    
    @patch('vidgen.models.video.create_fallback_image')
    @patch('vidgen.models.video.create_silent_audio')
    @patch('subprocess.run')
    def test_generate_video_segment_fallbacks(self, mock_subprocess, mock_silent, mock_fallback):
        """Test video generation with fallback image and audio"""
        mock_fallback.return_value = "/path/to/fallback.png"
        mock_silent.return_value = "/path/to/silent.wav"
        mock_subprocess.return_value = MagicMock()
        
        video_command = {
            "narration": "",
            "start": 0,
            "end": 3,
            "character_face": {}
        }
        
        with patch('vidgen.models.video.generate_character_image', return_value=None):
            with patch('vidgen.models.video.generate_tts_audio', return_value=None):
                result = generate_video_segment(video_command)
                assert result is not None
                
                mock_fallback.assert_called_once()
                mock_silent.assert_called_once()
    
    def test_generate_video_segment_face_cache(self):
        """Test face caching functionality"""
        face_cache = {}
        
        video_command = {
            "narration": "Test",
            "start": 0,
            "end": 2,
            "character_face": {
                "character": "alice",
                "face_prompt": "young woman",
                "seed": 123
            }
        }
        
        with patch('vidgen.models.video.generate_character_image', return_value="/cached/image.png") as mock_image:
            with patch('vidgen.models.video.generate_tts_audio', return_value="/audio.wav"):
                with patch('subprocess.run'):
                    # First call should generate image
                    generate_video_segment(video_command, face_cache)
                    assert ("alice", 123) in face_cache
                    
                    # Second call should use cache
                    generate_video_segment(video_command, face_cache)
                    mock_image.assert_called_once()  # Should only be called once
    
    @patch('subprocess.run')
    def test_generate_video_with_transitions_success(self, mock_subprocess):
        """Test video generation with transitions"""
        mock_subprocess.return_value = MagicMock()
        
        segments = ["video1.mp4", "video2.mp4", "video3.mp4"]
        result = generate_video_with_transitions(segments, "fade", 0.5)
        
        assert result is not None
        assert result.endswith('.mp4')
        mock_subprocess.assert_called_once()
    
    def test_generate_video_with_transitions_single_segment(self):
        """Test transitions with single segment returns original"""
        segments = ["single_video.mp4"]
        result = generate_video_with_transitions(segments)
        assert result == "single_video.mp4"
    
    def test_generate_video_with_transitions_empty_list(self):
        """Test transitions with empty list returns None"""
        result = generate_video_with_transitions([])
        assert result is None
    
    @patch('subprocess.run')
    def test_add_motion_effects_success(self, mock_subprocess):
        """Test adding motion effects to video"""
        mock_subprocess.return_value = MagicMock()
        
        result = add_motion_effects("input_video.mp4", "zoom_pan", 0.2)
        assert result is not None
        assert result.endswith('.mp4')
        mock_subprocess.assert_called_once()
    
    @patch('subprocess.run')
    def test_add_motion_effects_different_types(self, mock_subprocess):
        """Test different motion effect types"""
        mock_subprocess.return_value = MagicMock()
        
        effects = ["zoom_pan", "parallax", "shake"]
        for effect in effects:
            result = add_motion_effects("input.mp4", effect, 0.1)
            assert result is not None
    
    @patch('subprocess.run')
    def test_create_multi_angle_video_success(self, mock_subprocess):
        """Test multi-angle video creation"""
        mock_subprocess.return_value = MagicMock()
        
        result = create_multi_angle_video("image.png", "audio.wav", 6.0)
        assert result is not None
        assert result.endswith('.mp4')
        mock_subprocess.assert_called_once()
    
    @patch('subprocess.run')
    def test_create_multi_angle_video_custom_angles(self, mock_subprocess):
        """Test multi-angle video with custom angles"""
        mock_subprocess.return_value = MagicMock()
        
        custom_angles = [
            {"zoom": 2.0, "pan_x": 0.1, "pan_y": 0, "duration": 3.0},
            {"zoom": 1.0, "pan_x": -0.1, "pan_y": 0.1, "duration": 3.0}
        ]
        
        result = create_multi_angle_video("image.png", "audio.wav", 6.0, custom_angles)
        assert result is not None
    
    @patch('subprocess.run')
    def test_concatenate_videos_success(self, mock_subprocess):
        """Test video concatenation"""
        mock_subprocess.return_value = MagicMock()
        
        videos = ["video1.mp4", "video2.mp4", "video3.mp4"]
        result = concatenate_videos(videos)
        
        assert result is not None
        assert result.endswith('.mp4')
        mock_subprocess.assert_called_once()
    
    def test_concatenate_videos_single_video(self):
        """Test concatenation with single video returns original"""
        videos = ["single_video.mp4"]
        result = concatenate_videos(videos)
        assert result == "single_video.mp4"
    
    def test_concatenate_videos_empty_list(self):
        """Test concatenation with empty list returns None"""
        result = concatenate_videos([])
        assert result is None


class TestVideoFilters:
    
    def test_build_transition_filter_fade(self):
        """Test fade transition filter building"""
        segments = ["video1.mp4", "video2.mp4"]
        filter_str = _build_transition_filter(segments, "fade", 1.0)
        
        assert "xfade=transition=fade" in filter_str
        assert "duration=1.0" in filter_str
    
    def test_build_transition_filter_slide(self):
        """Test slide transition filter building"""
        segments = ["video1.mp4", "video2.mp4"]
        filter_str = _build_transition_filter(segments, "slide", 0.5)
        
        assert "xfade=transition=slideleft" in filter_str
        assert "duration=0.5" in filter_str
    
    def test_build_transition_filter_single_segment(self):
        """Test transition filter with single segment"""
        segments = ["video1.mp4"]
        filter_str = _build_transition_filter(segments, "fade", 1.0)
        
        assert filter_str == "[0:v][0:a]copy[out]"
    
    def test_create_zoom_pan_filter(self):
        """Test zoom and pan filter creation"""
        filter_str = _create_zoom_pan_filter(0.5)
        
        assert "zoompan" in filter_str
        assert "zoom" in filter_str
        assert "1280x720" in filter_str
    
    def test_create_parallax_filter(self):
        """Test parallax filter creation"""
        filter_str = _create_parallax_filter(0.3)
        
        assert "crop" in filter_str
        assert "1280:720" in filter_str
    
    def test_create_shake_filter(self):
        """Test shake filter creation"""
        filter_str = _create_shake_filter(0.2)
        
        assert "crop" in filter_str
        assert "sin" in filter_str
        assert "cos" in filter_str


class TestVideoFallbacks:
    
    @patch('PIL.Image.new')
    @patch('PIL.ImageDraw.Draw')
    def test_create_fallback_image_success(self, mock_draw, mock_image):
        """Test successful fallback image creation"""
        mock_img = MagicMock()
        mock_image.return_value = mock_img
        mock_draw.return_value = MagicMock()
        
        result = create_fallback_image()
        assert result is not None
        assert result.endswith('.png')
        mock_img.save.assert_called_once()
    
    def test_create_fallback_image_no_pil(self):
        """Test fallback image creation without PIL"""
        with patch('PIL.Image.new', side_effect=ImportError("No PIL")):
            result = create_fallback_image()
            assert result == "placeholder_image.png"
    
    @patch('subprocess.run')
    def test_create_silent_audio_success(self, mock_subprocess):
        """Test successful silent audio creation"""
        mock_subprocess.return_value = MagicMock()
        
        result = create_silent_audio(3.5)
        assert result is not None
        assert result.endswith('.wav')
        mock_subprocess.assert_called_once()
    
    @patch('subprocess.run')
    def test_create_silent_audio_ffmpeg_error(self, mock_subprocess):
        """Test silent audio creation with FFmpeg error"""
        mock_subprocess.side_effect = Exception("FFmpeg failed")
        
        result = create_silent_audio(2.0)
        assert result is None


class TestVideoErrorHandling:
    
    @patch('subprocess.run')
    def test_generate_video_segment_ffmpeg_error(self, mock_subprocess):
        """Test handling of FFmpeg errors in video generation"""
        mock_subprocess.side_effect = Exception("FFmpeg command failed")
        
        video_command = {
            "narration": "Test",
            "start": 0,
            "end": 2,
            "character_face": {}
        }
        
        with patch('vidgen.models.video.generate_character_image', return_value="image.png"):
            with patch('vidgen.models.video.generate_tts_audio', return_value="audio.wav"):
                with pytest.raises(Exception):
                    generate_video_segment(video_command)
    
    @patch('vidgen.models.video.concatenate_videos')
    @patch('subprocess.run')
    def test_generate_video_with_transitions_fallback(self, mock_subprocess, mock_concat):
        """Test fallback to concatenation when transitions fail"""
        mock_subprocess.side_effect = Exception("Transition failed")
        mock_concat.return_value = "concatenated.mp4"
        
        segments = ["video1.mp4", "video2.mp4"]
        result = generate_video_with_transitions(segments)
        
        assert result == "concatenated.mp4"
        mock_concat.assert_called_once_with(segments)
    
    @patch('subprocess.run')
    def test_add_motion_effects_error_returns_original(self, mock_subprocess):
        """Test that motion effects error returns original video"""
        mock_subprocess.side_effect = Exception("Motion effect failed")
        
        original_video = "original.mp4"
        result = add_motion_effects(original_video, "zoom_pan", 0.1)
        
        assert result == original_video


if __name__ == "__main__":
    pytest.main([__file__])
