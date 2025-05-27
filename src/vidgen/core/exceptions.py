"""
Custom exceptions for VidGen
"""

class VidGenException(Exception):
    """Base exception for VidGen"""
    def __init__(self, message, original_exception=None, recovery_suggestion=None):
        super().__init__(message)
        self.original_exception = original_exception
        self.recovery_suggestion = recovery_suggestion

class ScriptParsingError(VidGenException):
    """Raised when script parsing fails"""
    pass

class ModelLoadError(VidGenException):
    """Raised when model loading fails"""
    pass

class AudioGenerationError(VidGenException):
    """Raised when audio generation fails"""
    pass

class ImageGenerationError(VidGenException):
    """Raised when image generation fails"""
    pass

class VideoAssemblyError(VidGenException):
    """Raised when video assembly fails"""
    pass

class ConfigurationError(VidGenException):
    """Raised when configuration is invalid"""
    pass

class FFmpegError(VidGenException):
    """Raised when FFmpeg operations fail"""
    pass

class APIError(VidGenException):
    """Raised when external API calls fail"""
    pass

class FileSystemError(VidGenException):
    """Raised when file system operations fail"""
    pass

class MemoryError(VidGenException):
    """Raised when memory management issues occur"""
    pass

class DependencyError(VidGenException):
    """Raised when required dependencies are missing"""
    pass

# Error recovery utilities
class ErrorRecovery:
    """Utilities for error recovery and fallback mechanisms"""
    
    @staticmethod
    def create_user_friendly_message(exception):
        """Convert technical exceptions to user-friendly messages"""
        if isinstance(exception, ModelLoadError):
            return "AI model loading failed. Please check your GPU memory or switch to CPU mode."
        elif isinstance(exception, FFmpegError):
            return "Video processing failed. Please ensure FFmpeg is installed and accessible."
        elif isinstance(exception, APIError):
            return "External service is unavailable. Please check your internet connection and API keys."
        elif isinstance(exception, FileSystemError):
            return "File access failed. Please check file permissions and available disk space."
        elif isinstance(exception, DependencyError):
            return "Required software is missing. Please run the setup script to install dependencies."
        else:
            return f"An unexpected error occurred: {str(exception)}"
    
    @staticmethod
    def suggest_recovery_action(exception):
        """Suggest recovery actions for different error types"""
        if isinstance(exception, ModelLoadError):
            return "Try reducing model size or switching to CPU mode in settings."
        elif isinstance(exception, FFmpegError):
            return "Install FFmpeg or check the installation path in your system PATH."
        elif isinstance(exception, APIError):
            return "Check your API keys in the configuration and verify internet connectivity."
        elif isinstance(exception, FileSystemError):
            return "Ensure write permissions to output directory and sufficient disk space."
        elif isinstance(exception, MemoryError):
            return "Close other applications or reduce batch size to free up memory."
        else:
            return "Please check the logs for more details and try again."
    
    @staticmethod
    def get_fallback_strategy(operation_type):
        """Get fallback strategies for different operation types"""
        strategies = {
            "image_generation": "Use placeholder image or simple colored background",
            "audio_generation": "Generate silent audio or simple tone",
            "video_assembly": "Create static video with image and audio",
            "api_call": "Use cached result or simplified processing",
            "model_load": "Use lighter model or CPU fallback"
        }
        return strategies.get(operation_type, "Continue with reduced functionality")

# Decorator for automatic error handling and recovery
def with_error_recovery(fallback_func=None, recovery_strategy=None):
    """
    Decorator to add automatic error handling and recovery to functions.
    
    Args:
        fallback_func: Function to call if the main function fails
        recovery_strategy: Strategy to use for recovery
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log the error
                import logging
                logger = logging.getLogger(f"VidGen.{func.__module__}.{func.__name__}")
                logger.error(f"Function {func.__name__} failed: {e}")
                
                # Try recovery
                if fallback_func:
                    try:
                        logger.info(f"Attempting fallback for {func.__name__}")
                        return fallback_func(*args, **kwargs)
                    except Exception as fallback_error:
                        logger.error(f"Fallback also failed: {fallback_error}")
                
                # Re-raise with enhanced error information
                if isinstance(e, VidGenException):
                    raise e
                else:
                    raise VidGenException(
                        f"Unexpected error in {func.__name__}: {str(e)}",
                        original_exception=e,
                        recovery_suggestion=ErrorRecovery.suggest_recovery_action(e)
                    )
        return wrapper
    return decorator
