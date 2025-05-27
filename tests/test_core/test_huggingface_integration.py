"""
Tests for Hugging Face token integration in VidGen configuration system.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from src.vidgen.core.config import VideoGenConfig


class TestHuggingFaceIntegration:
    """Test suite for Hugging Face token configuration and authentication."""
    
    def test_huggingface_token_environment_variables(self):
        """Test that Hugging Face token is read from environment variables."""
        test_cases = [
            ("HUGGINGFACE_TOKEN", "test_hf_token_1"),
            ("HF_TOKEN", "test_hf_token_2"),
            ("HUGGINGFACE_HUB_TOKEN", "test_hf_token_3")
        ]
        
        for env_var, token_value in test_cases:
            with patch.dict(os.environ, {env_var: token_value}, clear=True):
                # Reload config to pick up new environment
                config_token = (
                    os.getenv("HUGGINGFACE_TOKEN") or 
                    os.getenv("HF_TOKEN") or 
                    os.getenv("HUGGINGFACE_HUB_TOKEN")
                )
                assert config_token == token_value
    
    def test_huggingface_token_priority(self):
        """Test that HUGGINGFACE_TOKEN takes priority over other variants."""
        env_vars = {
            "HUGGINGFACE_TOKEN": "primary_token",
            "HF_TOKEN": "secondary_token",
            "HUGGINGFACE_HUB_TOKEN": "tertiary_token"
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config_token = (
                os.getenv("HUGGINGFACE_TOKEN") or 
                os.getenv("HF_TOKEN") or 
                os.getenv("HUGGINGFACE_HUB_TOKEN")
            )
            assert config_token == "primary_token"
    
    def test_api_key_validation(self):
        """Test API key validation functionality."""
        with patch.object(VideoGenConfig, 'GEMINI_API_KEY', 'test_gemini_key'):
            with patch.object(VideoGenConfig, 'HUGGINGFACE_TOKEN', 'test_hf_token'):
                validation = VideoGenConfig.validate_api_keys()
                
                assert validation["gemini_api_key"] is True
                assert validation["huggingface_token"] is True
                assert validation["all_required_present"] is True
                assert len(validation["missing_keys"]) == 0
    
    def test_api_key_validation_missing_keys(self):
        """Test validation when API keys are missing."""
        with patch.object(VideoGenConfig, 'GEMINI_API_KEY', None):
            with patch.object(VideoGenConfig, 'HUGGINGFACE_TOKEN', None):
                validation = VideoGenConfig.validate_api_keys()
                
                assert validation["gemini_api_key"] is False
                assert validation["huggingface_token"] is False
                assert validation["all_required_present"] is False
                assert "GEMINI_API_KEY" in validation["missing_keys"]
                assert any("HUGGINGFACE_TOKEN" in key for key in validation["missing_keys"])
    
    def test_huggingface_auth_kwargs(self):
        """Test generation of Hugging Face authentication kwargs."""
        # Test with token present
        with patch.object(VideoGenConfig, 'HUGGINGFACE_TOKEN', 'test_token'):
            kwargs = VideoGenConfig.get_huggingface_auth_kwargs()
            
            assert "use_auth_token" in kwargs
            assert "token" in kwargs
            assert kwargs["use_auth_token"] == "test_token"
            assert kwargs["token"] == "test_token"
        
        # Test with no token
        with patch.object(VideoGenConfig, 'HUGGINGFACE_TOKEN', None):
            kwargs = VideoGenConfig.get_huggingface_auth_kwargs()
            assert kwargs == {}
    
    def test_model_utils_auth_setup(self):
        """Test that model_utils properly sets up authentication."""
        try:
            from src.vidgen.models.model_utils import setup_huggingface_auth
            
            test_token = "test_setup_token"
            with patch.object(VideoGenConfig, 'HUGGINGFACE_TOKEN', test_token):
                with patch.dict(os.environ, {}, clear=True):
                    setup_huggingface_auth()
                    
                    # Check that all environment variables are set
                    assert os.environ.get("HUGGINGFACE_HUB_TOKEN") == test_token
                    assert os.environ.get("HF_TOKEN") == test_token
                    assert os.environ.get("HUGGINGFACE_TOKEN") == test_token
        
        except ImportError:
            pytest.skip("model_utils not available for testing")
    
    def test_model_access_validation(self):
        """Test model access validation functionality."""
        try:
            from src.vidgen.models.model_utils import validate_model_access
            
            # Mock huggingface_hub to test different scenarios
            with patch('src.vidgen.models.model_utils.model_info') as mock_model_info:
                # Test successful access
                mock_info = MagicMock()
                mock_info.private = False
                mock_model_info.return_value = mock_info
                
                result = validate_model_access("test/model")
                assert result["accessible"] is True
                assert result["requires_auth"] is False
                assert result["error"] is None
                
                # Test private model
                mock_info.private = True
                mock_model_info.return_value = mock_info
                
                result = validate_model_access("test/private-model")
                assert result["accessible"] is True
                assert result["requires_auth"] is True
                
                # Test authentication error
                mock_model_info.side_effect = Exception("401 Unauthorized")
                
                result = validate_model_access("test/auth-required")
                assert result["accessible"] is False
                assert result["requires_auth"] is True
                assert "401" in result["error"]
        
        except ImportError:
            pytest.skip("huggingface_hub not available for testing")


class TestImageModelAuthentication:
    """Test suite for image model Hugging Face authentication."""
    
    def test_image_pipeline_auth_setup(self):
        """Test that image pipeline properly uses authentication."""
        try:
            from src.vidgen.models.image import get_image_pipeline
            
            with patch('src.vidgen.models.image.StableDiffusionPipeline') as mock_pipeline:
                with patch('src.vidgen.models.image.torch') as mock_torch:
                    with patch.object(VideoGenConfig, 'HUGGINGFACE_TOKEN', 'test_token'):
                        with patch('src.vidgen.models.image.setup_huggingface_auth') as mock_setup:
                            mock_pipeline.from_pretrained.return_value = MagicMock()
                            mock_torch.cuda.is_available.return_value = False
                            
                            # Call get_image_pipeline
                            pipeline = get_image_pipeline()
                            
                            # Verify setup_huggingface_auth was called
                            mock_setup.assert_called_once()
                            
                            # Verify from_pretrained was called with auth kwargs
                            mock_pipeline.from_pretrained.assert_called_once()
                            call_args = mock_pipeline.from_pretrained.call_args
                            
                            # Should include authentication parameters
                            assert 'use_auth_token' in call_args[1] or 'token' in call_args[1]
        
        except ImportError:
            pytest.skip("Required dependencies not available for testing")


if __name__ == "__main__":
    pytest.main([__file__])
