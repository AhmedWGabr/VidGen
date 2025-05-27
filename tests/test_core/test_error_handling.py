"""
Tests for error handling and recovery mechanisms
"""
import pytest
from unittest.mock import patch, MagicMock

from vidgen.core.exceptions import (
    VidGenException,
    ScriptParsingError,
    ModelLoadError,
    AudioGenerationError,
    ImageGenerationError,
    VideoAssemblyError,
    ConfigurationError,
    FFmpegError,
    APIError,
    FileSystemError,
    MemoryError,
    DependencyError,
    ErrorRecovery,
    with_error_recovery
)


class TestCustomExceptions:
    
    def test_vidgen_exception_base(self):
        """Test base VidGenException functionality"""
        original_error = ValueError("Original error")
        recovery_msg = "Try restarting the application"
        
        exc = VidGenException(
            "Something went wrong",
            original_exception=original_error,
            recovery_suggestion=recovery_msg
        )
        
        assert str(exc) == "Something went wrong"
        assert exc.original_exception == original_error
        assert exc.recovery_suggestion == recovery_msg
    
    def test_specific_exceptions_inheritance(self):
        """Test that specific exceptions inherit from VidGenException"""
        exceptions = [
            ScriptParsingError,
            ModelLoadError,
            AudioGenerationError,
            ImageGenerationError,
            VideoAssemblyError,
            ConfigurationError,
            FFmpegError,
            APIError,
            FileSystemError,
            MemoryError,
            DependencyError
        ]
        
        for exc_class in exceptions:
            exc = exc_class("Test error")
            assert isinstance(exc, VidGenException)
    
    def test_exception_with_recovery_suggestion(self):
        """Test exceptions with recovery suggestions"""
        exc = ModelLoadError("GPU memory exhausted", recovery_suggestion="Switch to CPU mode")
        assert exc.recovery_suggestion == "Switch to CPU mode"


class TestErrorRecovery:
    
    def test_create_user_friendly_message_model_error(self):
        """Test user-friendly message for model errors"""
        exc = ModelLoadError("CUDA out of memory")
        message = ErrorRecovery.create_user_friendly_message(exc)
        
        assert "AI model loading failed" in message
        assert "GPU memory" in message
    
    def test_create_user_friendly_message_ffmpeg_error(self):
        """Test user-friendly message for FFmpeg errors"""
        exc = FFmpegError("ffmpeg command not found")
        message = ErrorRecovery.create_user_friendly_message(exc)
        
        assert "Video processing failed" in message
        assert "FFmpeg" in message
    
    def test_create_user_friendly_message_api_error(self):
        """Test user-friendly message for API errors"""
        exc = APIError("Connection timeout")
        message = ErrorRecovery.create_user_friendly_message(exc)
        
        assert "External service is unavailable" in message
        assert "internet connection" in message
    
    def test_create_user_friendly_message_filesystem_error(self):
        """Test user-friendly message for filesystem errors"""
        exc = FileSystemError("Permission denied")
        message = ErrorRecovery.create_user_friendly_message(exc)
        
        assert "File access failed" in message
        assert "permissions" in message
    
    def test_create_user_friendly_message_dependency_error(self):
        """Test user-friendly message for dependency errors"""
        exc = DependencyError("Missing required package")
        message = ErrorRecovery.create_user_friendly_message(exc)
        
        assert "Required software is missing" in message
        assert "setup script" in message
    
    def test_create_user_friendly_message_unknown_error(self):
        """Test user-friendly message for unknown errors"""
        exc = Exception("Unknown error")
        message = ErrorRecovery.create_user_friendly_message(exc)
        
        assert "An unexpected error occurred" in message
        assert "Unknown error" in message
    
    def test_suggest_recovery_action_model_error(self):
        """Test recovery suggestions for model errors"""
        exc = ModelLoadError("Model too large")
        suggestion = ErrorRecovery.suggest_recovery_action(exc)
        
        assert "CPU mode" in suggestion or "model size" in suggestion
    
    def test_suggest_recovery_action_ffmpeg_error(self):
        """Test recovery suggestions for FFmpeg errors"""
        exc = FFmpegError("FFmpeg not found")
        suggestion = ErrorRecovery.suggest_recovery_action(exc)
        
        assert "Install FFmpeg" in suggestion or "PATH" in suggestion
    
    def test_suggest_recovery_action_api_error(self):
        """Test recovery suggestions for API errors"""
        exc = APIError("Authentication failed")
        suggestion = ErrorRecovery.suggest_recovery_action(exc)
        
        assert "API keys" in suggestion or "internet" in suggestion
    
    def test_suggest_recovery_action_filesystem_error(self):
        """Test recovery suggestions for filesystem errors"""
        exc = FileSystemError("Disk full")
        suggestion = ErrorRecovery.suggest_recovery_action(exc)
        
        assert "permissions" in suggestion or "disk space" in suggestion
    
    def test_suggest_recovery_action_memory_error(self):
        """Test recovery suggestions for memory errors"""
        exc = MemoryError("Out of memory")
        suggestion = ErrorRecovery.suggest_recovery_action(exc)
        
        assert "applications" in suggestion or "batch size" in suggestion
    
    def test_suggest_recovery_action_unknown_error(self):
        """Test recovery suggestions for unknown errors"""
        exc = Exception("Random error")
        suggestion = ErrorRecovery.suggest_recovery_action(exc)
        
        assert "logs" in suggestion or "try again" in suggestion
    
    def test_get_fallback_strategy(self):
        """Test fallback strategy suggestions"""
        strategies = {
            "image_generation": "placeholder image",
            "audio_generation": "silent audio",
            "video_assembly": "static video",
            "api_call": "cached result",
            "model_load": "lighter model"
        }
        
        for operation, expected_keyword in strategies.items():
            strategy = ErrorRecovery.get_fallback_strategy(operation)
            assert expected_keyword in strategy
    
    def test_get_fallback_strategy_unknown_operation(self):
        """Test fallback strategy for unknown operation"""
        strategy = ErrorRecovery.get_fallback_strategy("unknown_operation")
        assert "reduced functionality" in strategy


class TestErrorRecoveryDecorator:
    
    def test_with_error_recovery_success(self):
        """Test decorator with successful function execution"""
        @with_error_recovery()
        def successful_function(x, y):
            return x + y
        
        result = successful_function(2, 3)
        assert result == 5
    
    def test_with_error_recovery_with_fallback(self):
        """Test decorator with fallback function"""
        def fallback_function(x, y):
            return x * y  # Different operation as fallback
        
        @with_error_recovery(fallback_func=fallback_function)
        def failing_function(x, y):
            raise ValueError("Function failed")
        
        result = failing_function(2, 3)
        assert result == 6  # Should use fallback (multiplication)
    
    def test_with_error_recovery_vidgen_exception_passthrough(self):
        """Test that VidGenExceptions are passed through unchanged"""
        @with_error_recovery()
        def function_with_vidgen_error():
            raise ModelLoadError("Model failed to load")
        
        with pytest.raises(ModelLoadError) as exc_info:
            function_with_vidgen_error()
        
        assert str(exc_info.value) == "Model failed to load"
    
    def test_with_error_recovery_unknown_exception_wrapped(self):
        """Test that unknown exceptions are wrapped in VidGenException"""
        @with_error_recovery()
        def function_with_unknown_error():
            raise ValueError("Unknown error")
        
        with pytest.raises(VidGenException) as exc_info:
            function_with_unknown_error()
        
        assert "Unexpected error" in str(exc_info.value)
        assert isinstance(exc_info.value.original_exception, ValueError)
    
    @patch('logging.getLogger')
    def test_with_error_recovery_logging(self, mock_get_logger):
        """Test that decorator logs errors appropriately"""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        @with_error_recovery()
        def failing_function():
            raise ValueError("Test error")
        
        with pytest.raises(VidGenException):
            failing_function()
        
        # Should have logged the error
        mock_logger.error.assert_called_once()
    
    def test_with_error_recovery_fallback_also_fails(self):
        """Test behavior when both main function and fallback fail"""
        def failing_fallback():
            raise RuntimeError("Fallback also failed")
        
        @with_error_recovery(fallback_func=failing_fallback)
        def failing_function():
            raise ValueError("Main function failed")
        
        with pytest.raises(VidGenException) as exc_info:
            failing_function()
        
        # Should still raise the original error wrapped in VidGenException
        assert isinstance(exc_info.value.original_exception, ValueError)
    
    @patch('logging.getLogger')
    def test_with_error_recovery_fallback_logging(self, mock_get_logger):
        """Test logging when fallback is attempted"""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        def working_fallback():
            return "fallback result"
        
        @with_error_recovery(fallback_func=working_fallback)
        def failing_function():
            raise ValueError("Main function failed")
        
        result = failing_function()
        assert result == "fallback result"
        
        # Should log both the error and the fallback attempt
        assert mock_logger.error.called
        assert mock_logger.info.called


class TestIntegrationWithExistingCode:
    
    def test_exception_with_context_preservation(self):
        """Test that exceptions preserve context through the system"""
        original_error = ConnectionError("Network failed")
        api_error = APIError(
            "Gemini API call failed",
            original_exception=original_error,
            recovery_suggestion="Check your internet connection"
        )
        
        # Test that all information is preserved
        assert "Gemini API call failed" in str(api_error)
        assert api_error.original_exception == original_error
        assert "internet connection" in api_error.recovery_suggestion
        
        # Test user-friendly message generation
        user_message = ErrorRecovery.create_user_friendly_message(api_error)
        assert "External service is unavailable" in user_message
        
        # Test recovery suggestion
        recovery = ErrorRecovery.suggest_recovery_action(api_error)
        assert "API keys" in recovery or "internet" in recovery


if __name__ == "__main__":
    pytest.main([__file__])
