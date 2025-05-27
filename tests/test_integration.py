"""
Integration tests for the complete VidGen pipeline
"""
import pytest
import os
import tempfile
import json
from unittest.mock import patch, MagicMock

from vidgen.main import generate_video_async, demo
from vidgen.services.script_parser import parse_detailed_script
from vidgen.services.gemini_api import call_gemini_api
from vidgen.models.tts import generate_tts_audio
from vidgen.models.image import generate_character_image
from vidgen.models.audio import generate_background_audio
from vidgen.models.video import generate_video_segment
from vidgen.services.video_assembler import assemble_video


class TestPipelineIntegration:
    
    @pytest.fixture
    def sample_script(self):
        """Sample script for testing"""
        return """
        FADE IN:

        NARRATOR (V.O.)
        Welcome to the world of artificial intelligence.

        The scene shows a futuristic laboratory with blinking lights.

        SCIENTIST
        Our breakthrough in machine learning will change everything.

        FADE OUT.
        """
    
    @pytest.fixture
    def sample_parsed_script(self):
        """Sample parsed script structure"""
        return {
            "segments": [
                {
                    "narration": "Welcome to the world of artificial intelligence.",
                    "start": 0,
                    "end": 3,
                    "character_face": {
                        "character": "narrator",
                        "face_prompt": "professional narrator",
                        "seed": 42
                    }
                },
                {
                    "narration": "Our breakthrough in machine learning will change everything.",
                    "start": 3,
                    "end": 7,
                    "character_face": {
                        "character": "scientist",
                        "face_prompt": "young scientist in lab coat",
                        "seed": 123
                    }
                }
            ],
            "audio": [
                "laboratory ambience with quiet beeping",
                "tech facility background noise"
            ],
            "video": [
                "futuristic laboratory with blinking lights",
                "close-up of scientist working"
            ]
        }
    
    @patch('vidgen.services.gemini_api.call_gemini_api')
    def test_script_parsing_integration(self, mock_gemini, sample_script, sample_parsed_script):
        """Test complete script parsing pipeline"""
        # Mock Gemini API response
        mock_gemini.return_value = json.dumps(sample_parsed_script)
        
        result = parse_detailed_script(sample_script, "test-api-key")
        
        assert result is not None
        assert "segments" in result
        assert "audio" in result
        assert "video" in result
        assert len(result["segments"]) == 2
        mock_gemini.assert_called_once()
    
    @patch('vidgen.models.tts.load_model')
    @patch('subprocess.run')
    def test_audio_generation_integration(self, mock_subprocess, mock_load_model, sample_parsed_script):
        """Test audio generation pipeline"""
        mock_load_model.return_value = (MagicMock(), MagicMock())
        mock_subprocess.return_value = MagicMock()
        
        # Test TTS generation
        tts_result = generate_tts_audio("Hello world")
        assert tts_result is not None
        
        # Test background audio generation
        bg_result = generate_background_audio("laboratory ambience")
        assert bg_result is not None
    
    @patch('diffusers.StableDiffusionPipeline.from_pretrained')
    def test_image_generation_integration(self, mock_pipeline):
        """Test image generation pipeline"""
        mock_pipe = MagicMock()
        mock_image = MagicMock()
        mock_pipe.return_value.images = [mock_image]
        mock_pipeline.return_value = mock_pipe
        
        result = generate_character_image("young scientist", seed=42)
        assert result is not None
    
    @patch('vidgen.models.video.generate_character_image')
    @patch('vidgen.models.video.generate_tts_audio')
    @patch('subprocess.run')
    def test_video_generation_integration(self, mock_subprocess, mock_tts, mock_image):
        """Test video generation pipeline"""
        mock_image.return_value = "/path/to/image.png"
        mock_tts.return_value = "/path/to/audio.wav"
        mock_subprocess.return_value = MagicMock()
        
        video_command = {
            "narration": "Test narration",
            "start": 0,
            "end": 3,
            "character_face": {
                "character": "narrator",
                "face_prompt": "professional person",
                "seed": 42
            }
        }
        
        result = generate_video_segment(video_command)
        assert result is not None
        assert result.endswith('.mp4')
    
    @patch('subprocess.run')
    def test_video_assembly_integration(self, mock_subprocess):
        """Test video assembly pipeline"""
        mock_subprocess.return_value = MagicMock()
        
        video_segments = ["segment1.mp4", "segment2.mp4"]
        background_audio = ["bg1.wav", "bg2.wav"]
        
        result = assemble_video(video_segments, background_audio)
        assert result is not None
        assert result.endswith('.mp4')
    
    @patch('vidgen.services.script_parser.parse_detailed_script')
    @patch('vidgen.models.tts.generate_tts_audio')
    @patch('vidgen.models.image.generate_character_image')
    @patch('vidgen.models.audio.generate_background_audio')
    @patch('vidgen.models.video.generate_video_segment')
    @patch('vidgen.services.video_assembler.assemble_video')
    async def test_full_pipeline_integration(
        self, 
        mock_assemble, 
        mock_video, 
        mock_bg_audio, 
        mock_image, 
        mock_tts, 
        mock_parse,
        sample_script,
        sample_parsed_script
    ):
        """Test the complete end-to-end pipeline"""
        # Setup mocks
        mock_parse.return_value = sample_parsed_script
        mock_tts.return_value = "/path/to/tts.wav"
        mock_image.return_value = "/path/to/image.png"
        mock_bg_audio.return_value = "/path/to/bg_audio.wav"
        mock_video.return_value = "/path/to/video.mp4"
        mock_assemble.return_value = "/path/to/final_video.mp4"
        
        # Run the full pipeline
        result = await generate_video_async(
            script=sample_script,
            gemini_api_key="test-key",
            segment_duration=5,
            seed=42
        )
        
        # Verify all steps were called
        mock_parse.assert_called_once()
        assert mock_tts.call_count >= 1
        assert mock_image.call_count >= 1
        assert mock_bg_audio.call_count >= 1
        assert mock_video.call_count >= 1
        mock_assemble.assert_called_once()
        
        # Verify result
        assert result is not None
        assert result.endswith('.mp4')
    
    @patch('vidgen.main.generate_video_async')
    def test_demo_function_integration(self, mock_generate_async):
        """Test the demo function integration"""
        mock_generate_async.return_value = "/path/to/demo_video.mp4"
        
        result = demo(
            script="Test script",
            gemini_api_key="test-key",
            segment_duration=3,
            seed=123
        )
        
        mock_generate_async.assert_called_once()
        assert result == "/path/to/demo_video.mp4"


class TestErrorHandlingIntegration:
    
    @patch('vidgen.services.script_parser.parse_detailed_script')
    async def test_script_parsing_error_recovery(self, mock_parse):
        """Test error recovery when script parsing fails"""
        from vidgen.core.exceptions import ScriptParsingError
        
        mock_parse.side_effect = ScriptParsingError("Invalid script format")
        
        with pytest.raises(ScriptParsingError):
            await generate_video_async(
                script="Invalid script",
                gemini_api_key="test-key",
                segment_duration=5,
                seed=42
            )
    
    @patch('vidgen.services.script_parser.parse_detailed_script')
    @patch('vidgen.models.tts.generate_tts_audio')
    async def test_partial_failure_recovery(self, mock_tts, mock_parse):
        """Test recovery when some components fail"""
        # Setup: parsing succeeds, TTS fails for some segments
        mock_parse.return_value = {
            "segments": [
                {"narration": "First segment", "start": 0, "end": 2, "character_face": {}},
                {"narration": "Second segment", "start": 2, "end": 4, "character_face": {}}
            ],
            "audio": ["background sound"],
            "video": ["scene description"]
        }
        
        # TTS fails for second call
        mock_tts.side_effect = ["/path/to/audio1.wav", None]
        
        with patch('vidgen.models.image.generate_character_image', return_value="/image.png"):
            with patch('vidgen.models.audio.generate_background_audio', return_value="/bg.wav"):
                with patch('vidgen.models.video.generate_video_segment', return_value="/video.mp4"):
                    with patch('vidgen.services.video_assembler.assemble_video', return_value="/final.mp4"):
                        result = await generate_video_async(
                            script="Test script",
                            gemini_api_key="test-key",
                            segment_duration=5,
                            seed=42
                        )
                        
                        # Should still produce a result despite partial failures
                        assert result is not None
    
    @patch('vidgen.services.script_parser.parse_detailed_script')
    @patch('vidgen.models.tts.generate_tts_audio')
    @patch('vidgen.models.image.generate_character_image') 
    @patch('vidgen.models.audio.generate_background_audio')
    @patch('vidgen.models.video.generate_video_segment')
    async def test_model_loading_error_recovery(
        self, 
        mock_video, 
        mock_bg_audio, 
        mock_image, 
        mock_tts, 
        mock_parse
    ):
        """Test recovery when model loading fails"""
        from vidgen.core.exceptions import ModelLoadError
        
        mock_parse.return_value = {
            "segments": [{"narration": "Test", "start": 0, "end": 2, "character_face": {}}],
            "audio": ["background"],
            "video": ["scene"]
        }
        
        # Image generation fails due to model loading
        mock_image.side_effect = ModelLoadError("GPU memory exhausted")
        mock_tts.return_value = "/audio.wav"
        mock_bg_audio.return_value = "/bg.wav"
        mock_video.return_value = "/video.mp4"
        
        with patch('vidgen.services.video_assembler.assemble_video', return_value="/final.mp4"):
            # Should handle the model error gracefully
            result = await generate_video_async(
                script="Test script",
                gemini_api_key="test-key", 
                segment_duration=5,
                seed=42
            )
            
            # Should still produce result with fallback image
            assert result is not None


class TestPerformanceIntegration:
    
    @patch('vidgen.services.script_parser.parse_detailed_script')
    async def test_large_script_handling(self, mock_parse):
        """Test handling of large scripts with many segments"""
        # Create a large parsed script
        large_script = {
            "segments": [
                {
                    "narration": f"Segment {i} narration",
                    "start": i * 2,
                    "end": (i + 1) * 2,
                    "character_face": {"character": f"char{i}", "face_prompt": f"person {i}", "seed": i}
                }
                for i in range(10)  # 10 segments
            ],
            "audio": [f"background audio {i}" for i in range(10)],
            "video": [f"scene description {i}" for i in range(10)]
        }
        
        mock_parse.return_value = large_script
        
        with patch('vidgen.models.tts.generate_tts_audio', return_value="/audio.wav"):
            with patch('vidgen.models.image.generate_character_image', return_value="/image.png"):
                with patch('vidgen.models.audio.generate_background_audio', return_value="/bg.wav"):
                    with patch('vidgen.models.video.generate_video_segment', return_value="/video.mp4"):
                        with patch('vidgen.services.video_assembler.assemble_video', return_value="/final.mp4"):
                            result = await generate_video_async(
                                script="Large script",
                                gemini_api_key="test-key",
                                segment_duration=5,
                                seed=42
                            )
                            
                            assert result is not None
    
    async def test_concurrent_processing(self):
        """Test that concurrent processing works correctly"""
        import asyncio
        
        # Mock all the generation functions
        with patch('vidgen.services.script_parser.parse_detailed_script') as mock_parse:
            mock_parse.return_value = {
                "segments": [{"narration": "Test", "start": 0, "end": 2, "character_face": {}}],
                "audio": ["background"],
                "video": ["scene"]
            }
            
            with patch('vidgen.models.tts.generate_tts_audio', return_value="/audio.wav"):
                with patch('vidgen.models.image.generate_character_image', return_value="/image.png"):
                    with patch('vidgen.models.audio.generate_background_audio', return_value="/bg.wav"):
                        with patch('vidgen.models.video.generate_video_segment', return_value="/video.mp4"):
                            with patch('vidgen.services.video_assembler.assemble_video', return_value="/final.mp4"):
                                # Run multiple video generations concurrently
                                tasks = [
                                    generate_video_async("Script 1", "key", 5, 1),
                                    generate_video_async("Script 2", "key", 5, 2),
                                    generate_video_async("Script 3", "key", 5, 3)
                                ]
                                
                                results = await asyncio.gather(*tasks)
                                
                                # All should succeed
                                assert len(results) == 3
                                assert all(result is not None for result in results)


if __name__ == "__main__":
    pytest.main([__file__])
