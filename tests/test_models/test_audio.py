"""
Tests for audio generation functionality
"""
import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock

from vidgen.models.audio import (
    generate_background_audio, 
    mix_audio,
    _analyze_audio_command,
    _generate_silence,
    _generate_ambient_audio,
    _generate_music_audio
)
from vidgen.core.exceptions import AudioGenerationError


class TestAudioGeneration:
    
    def test_analyze_audio_command_silence(self):
        """Test analysis of silence commands"""
        audio_type, duration, frequency = _analyze_audio_command("silence")
        assert audio_type == "silence"
        assert duration == 5.0
        
    def test_analyze_audio_command_music(self):
        """Test analysis of music commands"""
        audio_type, duration, frequency = _analyze_audio_command("peaceful melody")
        assert audio_type == "music"
        
    def test_analyze_audio_command_ambient(self):
        """Test analysis of ambient commands"""
        audio_type, duration, frequency = _analyze_audio_command("laboratory ambience")
        assert audio_type == "ambient"
        
    def test_analyze_audio_command_with_duration(self):
        """Test duration extraction from commands"""
        audio_type, duration, frequency = _analyze_audio_command("ambient noise for 10 seconds")
        assert duration == 10.0
        
    def test_analyze_audio_command_frequency_patterns(self):
        """Test frequency pattern detection"""
        _, _, freq_low = _analyze_audio_command("deep rumbling sound")
        assert freq_low == "low"
        
        _, _, freq_high = _analyze_audio_command("bright chirping")
        assert freq_high == "high"
        
        _, _, freq_mid = _analyze_audio_command("voice in middle range")
        assert freq_mid == "mid"
    
    @patch('subprocess.run')
    def test_generate_silence_success(self, mock_subprocess):
        """Test successful silence generation"""
        mock_subprocess.return_value = MagicMock()
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            result = _generate_silence(tmp.name, 3.0)
            assert result == tmp.name
            mock_subprocess.assert_called_once()
        
        os.unlink(tmp.name)
    
    @patch('subprocess.run')
    def test_generate_ambient_audio_success(self, mock_subprocess):
        """Test successful ambient audio generation"""
        mock_subprocess.return_value = MagicMock()
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            result = _generate_ambient_audio(tmp.name, "laboratory ambience", 5.0, "low")
            assert result == tmp.name
            mock_subprocess.assert_called_once()
        
        os.unlink(tmp.name)
    
    @patch('subprocess.run')
    def test_generate_music_audio_success(self, mock_subprocess):
        """Test successful music generation"""
        mock_subprocess.return_value = MagicMock()
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            result = _generate_music_audio(tmp.name, "peaceful melody", 4.0)
            assert result == tmp.name
            mock_subprocess.assert_called_once()
        
        os.unlink(tmp.name)
    
    @patch('vidgen.models.audio._generate_silence')
    @patch('vidgen.models.audio._analyze_audio_command')
    def test_generate_background_audio_integration(self, mock_analyze, mock_silence):
        """Test full background audio generation flow"""
        mock_analyze.return_value = ("silence", 3.0, "low")
        mock_silence.return_value = "/path/to/audio.wav"
        
        result = generate_background_audio("quiet ambience")
        assert result == "/path/to/audio.wav"
        mock_analyze.assert_called_once_with("quiet ambience")
        mock_silence.assert_called_once()
    
    @patch('subprocess.run')
    def test_mix_audio_multiple_tracks(self, mock_subprocess):
        """Test mixing multiple audio tracks"""
        mock_subprocess.return_value = MagicMock()
        
        tracks = ["track1.wav", "track2.wav", "track3.wav"]
        levels = [1.0, 0.5, 0.3]
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            result = mix_audio(tracks, levels, tmp.name)
            assert result == tmp.name
            mock_subprocess.assert_called_once()
        
        os.unlink(tmp.name)
    
    def test_mix_audio_single_track(self):
        """Test mixing with single track returns original"""
        tracks = ["single_track.wav"]
        result = mix_audio(tracks)
        assert result == "single_track.wav"
    
    def test_mix_audio_empty_tracks(self):
        """Test mixing with no tracks returns None"""
        result = mix_audio([])
        assert result is None
    
    @patch('subprocess.run')
    def test_generate_background_audio_fallback_on_error(self, mock_subprocess):
        """Test fallback to silence when generation fails"""
        # First call fails, second succeeds (fallback)
        mock_subprocess.side_effect = [Exception("FFmpeg failed"), MagicMock()]
        
        result = generate_background_audio("some audio command")
        # Should return None if even fallback fails, but we're mocking success for fallback
        assert mock_subprocess.call_count == 2


class TestAudioErrorHandling:
    
    @patch('subprocess.run')
    def test_generate_background_audio_ffmpeg_error(self, mock_subprocess):
        """Test handling of FFmpeg errors"""
        mock_subprocess.side_effect = Exception("FFmpeg not found")
        
        result = generate_background_audio("test audio")
        assert result is None  # Should return None on error
    
    @patch('os.makedirs')
    def test_generate_background_audio_directory_error(self, mock_makedirs):
        """Test handling of directory creation errors"""
        mock_makedirs.side_effect = PermissionError("No write permission")
        
        result = generate_background_audio("test audio")
        assert result is None
    
    @patch('subprocess.run')
    def test_mix_audio_ffmpeg_error(self, mock_subprocess):
        """Test mix_audio fallback on FFmpeg error"""
        mock_subprocess.side_effect = Exception("FFmpeg failed")
        
        tracks = ["track1.wav", "track2.wav"]
        result = mix_audio(tracks)
        
        # Should return first track as fallback
        assert result == "track1.wav"


class TestAudioTypeDetection:
    
    def test_tech_keywords_detection(self):
        """Test detection of tech/laboratory keywords"""
        commands = [
            "laboratory ambience with quiet beeping",
            "tech facility background noise",
            "computer lab atmosphere"
        ]
        
        for command in commands:
            audio_type, _, _ = _analyze_audio_command(command)
            assert audio_type == "ambient"
    
    def test_nature_keywords_detection(self):
        """Test detection of nature keywords"""
        commands = [
            "forest ambience with birds",
            "nature sounds background",
            "countryside morning atmosphere"
        ]
        
        for command in commands:
            audio_type, _, _ = _analyze_audio_command(command)
            assert audio_type == "ambient"
    
    def test_music_keywords_detection(self):
        """Test detection of music keywords"""
        commands = [
            "peaceful melody",
            "background music",
            "soft tune playing",
            "gentle song"
        ]
        
        for command in commands:
            audio_type, _, _ = _analyze_audio_command(command)
            assert audio_type == "music"


if __name__ == "__main__":
    pytest.main([__file__])
