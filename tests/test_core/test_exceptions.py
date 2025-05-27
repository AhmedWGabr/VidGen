"""
Tests for VidGen custom exceptions.
"""

import pytest
from vidgen.core.exceptions import (
    VidGenError,
    ModelError,
    APIError,
    ConfigurationError,
    FileOperationError
)


class TestVidGenError:
    """Test base VidGenError exception."""
    
    def test_base_exception_creation(self):
        """Test basic exception creation."""
        error = VidGenError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)
    
    def test_base_exception_with_cause(self):
        """Test exception with underlying cause."""
        original_error = ValueError("Original error")
        error = VidGenError("Wrapper error", original_error)
        
        assert str(error) == "Wrapper error"
        assert error.__cause__ == original_error
    
    def test_base_exception_inheritance(self):
        """Test that all custom exceptions inherit from VidGenError."""
        assert issubclass(ModelError, VidGenError)
        assert issubclass(APIError, VidGenError)
        assert issubclass(ConfigurationError, VidGenError)
        assert issubclass(FileOperationError, VidGenError)


class TestModelError:
    """Test ModelError exception."""
    
    def test_model_error_creation(self):
        """Test ModelError creation."""
        error = ModelError("Model loading failed")
        assert str(error) == "Model loading failed"
        assert isinstance(error, VidGenError)
    
    def test_model_error_with_model_name(self):
        """Test ModelError with model name context."""
        error = ModelError("Loading failed", model_name="stable-diffusion")
        assert "stable-diffusion" in str(error) or hasattr(error, 'model_name')
    
    def test_model_error_with_operation(self):
        """Test ModelError with operation context."""
        error = ModelError("Operation failed", operation="text_to_image")
        assert "text_to_image" in str(error) or hasattr(error, 'operation')


class TestAPIError:
    """Test APIError exception."""
    
    def test_api_error_creation(self):
        """Test APIError creation."""
        error = APIError("API request failed")
        assert str(error) == "API request failed"
        assert isinstance(error, VidGenError)
    
    def test_api_error_with_status_code(self):
        """Test APIError with HTTP status code."""
        error = APIError("Request failed", status_code=404)
        assert "404" in str(error) or hasattr(error, 'status_code')
    
    def test_api_error_with_endpoint(self):
        """Test APIError with API endpoint context."""
        error = APIError("Request failed", endpoint="/api/generate")
        assert "/api/generate" in str(error) or hasattr(error, 'endpoint')


class TestConfigurationError:
    """Test ConfigurationError exception."""
    
    def test_configuration_error_creation(self):
        """Test ConfigurationError creation."""
        error = ConfigurationError("Invalid configuration")
        assert str(error) == "Invalid configuration"
        assert isinstance(error, VidGenError)
    
    def test_configuration_error_with_setting(self):
        """Test ConfigurationError with setting name."""
        error = ConfigurationError("Invalid value", setting="api_key")
        assert "api_key" in str(error) or hasattr(error, 'setting')
    
    def test_configuration_error_with_file(self):
        """Test ConfigurationError with config file context."""
        error = ConfigurationError("Parse error", config_file="config.json")
        assert "config.json" in str(error) or hasattr(error, 'config_file')


class TestFileOperationError:
    """Test FileOperationError exception."""
    
    def test_file_operation_error_creation(self):
        """Test FileOperationError creation."""
        error = FileOperationError("File operation failed")
        assert str(error) == "File operation failed"
        assert isinstance(error, VidGenError)
    
    def test_file_operation_error_with_path(self):
        """Test FileOperationError with file path."""
        error = FileOperationError("Cannot read file", file_path="/path/to/file.txt")
        assert "/path/to/file.txt" in str(error) or hasattr(error, 'file_path')
    
    def test_file_operation_error_with_operation(self):
        """Test FileOperationError with operation type."""
        error = FileOperationError("Operation failed", operation="write")
        assert "write" in str(error) or hasattr(error, 'operation')


class TestExceptionUsage:
    """Test practical exception usage scenarios."""
    
    def test_exception_chaining(self):
        """Test exception chaining with raise from."""
        original_error = FileNotFoundError("File not found")
        
        try:
            raise FileOperationError("Failed to load file") from original_error
        except FileOperationError as e:
            assert e.__cause__ == original_error
            assert isinstance(e, VidGenError)
    
    def test_exception_hierarchy_catching(self):
        """Test catching exceptions using base class."""
        model_error = ModelError("Model failed")
        api_error = APIError("API failed")
        
        # Should be able to catch both with base VidGenError
        for error in [model_error, api_error]:
            try:
                raise error
            except VidGenError as e:
                assert isinstance(e, VidGenError)
    
    def test_exception_context_preservation(self):
        """Test that exception context is preserved."""
        try:
            # Simulate nested operation that fails
            try:
                raise ValueError("Inner error")
            except ValueError as e:
                raise ModelError("Model operation failed") from e
        except ModelError as e:
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, ValueError)
            assert str(e.__cause__) == "Inner error"


if __name__ == "__main__":
    pytest.main([__file__])
