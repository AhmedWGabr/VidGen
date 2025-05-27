# Test for Gemini API service
"""
Tests for Gemini API service
"""

import pytest
from unittest.mock import patch, MagicMock
import json
import requests
from src.vidgen.services.gemini_api import call_gemini_api
from src.vidgen.core.config import VideoGenConfig

@pytest.fixture
def mock_response():
    """Mock response from Gemini API"""
    response = MagicMock()
    mock_data = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": json.dumps([
                                {
                                    "start": "00:00",
                                    "end": "00:05",
                                    "scene": "Countryside morning",
                                    "narration": "The sun rises over the peaceful countryside",
                                    "audio": "Gentle morning birds chirping",
                                    "visual": "Slow pan over green hills",
                                    "image": "Countryside with rolling hills and morning dew"
                                }
                            ])
                        }
                    ]
                }
            }
        ]
    }
    response.json.return_value = mock_data
    response.raise_for_status = MagicMock()
    return response

def test_call_gemini_api_success(mock_response):
    """Test successful Gemini API call"""
    # Arrange
    script = "A beautiful countryside morning"
    api_key = "test_api_key"
    segment_duration = 5
    
    # Mock the post request
    with patch('requests.post', return_value=mock_response) as mock_post:
        # Act
        result = call_gemini_api(script, api_key, segment_duration)
        
        # Assert
        mock_post.assert_called_once()
        # Check the URL used
        url_arg = mock_post.call_args[0][0]
        assert VideoGenConfig.GEMINI_MODEL in url_arg
        
        # Check API key in params
        params_arg = mock_post.call_args[1]['params']
        assert params_arg['key'] == api_key
        
        # Check that the prompt contains the segment duration
        data_arg = mock_post.call_args[1]['json']
        assert str(segment_duration) in data_arg['contents'][0]['parts'][0]['text']
        
        # Check the result
        assert result == mock_response.json.return_value

def test_call_gemini_api_error_handling():
    """Test error handling in Gemini API"""
    # Arrange
    script = "A beautiful countryside morning"
    api_key = "test_api_key"
    
    # Mock the post request to raise an exception
    with patch('requests.post', side_effect=requests.RequestException("API Error")) as mock_post, \
         patch('logging.getLogger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Act
        result = call_gemini_api(script, api_key)
        
        # Assert
        mock_post.assert_called_once()
        mock_logger.error.assert_called_once()
        assert "API Error" in mock_logger.error.call_args[0][0]
        assert result is None

def test_call_gemini_api_timeout():
    """Test timeout handling in Gemini API"""
    # Arrange
    script = "A beautiful countryside morning"
    api_key = "test_api_key"
    
    # Mock the post request to raise a timeout exception
    with patch('requests.post', side_effect=requests.Timeout("Connection timed out")), \
         patch('logging.getLogger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Act
        result = call_gemini_api(script, api_key)
        
        # Assert
        mock_logger.error.assert_called_once()
        assert "Connection timed out" in str(mock_logger.error.call_args[0][0])
        assert result is None

def test_call_gemini_api_http_error():
    """Test HTTP error handling in Gemini API"""
    # Arrange
    script = "A beautiful countryside morning"
    api_key = "test_api_key"
    
    # Create a response that will raise an HTTPError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Client Error")
    
    # Mock the post request
    with patch('requests.post', return_value=mock_response), \
         patch('logging.getLogger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Act
        result = call_gemini_api(script, api_key)
        
        # Assert
        mock_logger.error.assert_called_once()
        assert "404 Client Error" in str(mock_logger.error.call_args[0][0])
        assert result is None
