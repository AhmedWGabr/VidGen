"""
Tests for script parser service
"""

import pytest
import json
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from vidgen.services.script_parser import parse_detailed_script, validate_segment
from vidgen.models.data_models import ScriptSegment, Character
from vidgen.core.exceptions import ScriptParsingError

# Mock data for tests
VALID_SEGMENT = {
    "start": 0,
    "end": 5,
    "narration": "The day comes to an end",
    "scene": "A sunset over the ocean",
    "audio": "Soft piano music",
    "visual": "Wide shot of ocean horizon",
    "image": "Sunset: Orange and red sky over calm water"
}

MULTIPLE_SEGMENTS = [
    {
        "start": 0,
        "end": 5,
        "narration": "The day comes to an end",
        "scene": "A sunset over the ocean",
        "image": "Sunset: Orange and red sky over calm water"
    },
    {
        "start": 5,
        "end": 10,
        "narration": "As night approaches",
        "scene": "Stars beginning to appear",
        "image": "Night Sky: Dark blue with emerging stars"
    }
]

def test_parse_detailed_script_basic():
    """Test basic script parsing functionality"""
    # Mock Gemini API response
    mock_response = json.dumps([VALID_SEGMENT])
    
    result = parse_detailed_script(mock_response)
    
    assert result is not None
    assert "video" in result
    assert "tts" in result
    assert "audio" in result
    assert "image" in result
    assert len(result["video"]) == 1
    assert len(result["tts"]) == 1
    assert len(result["audio"]) == 1

def test_parse_detailed_script_multiple_segments():
    """Test parsing multiple script segments"""
    mock_response = json.dumps(MULTIPLE_SEGMENTS)
    
    result = parse_detailed_script(mock_response)
    
    assert result is not None
    assert len(result["video"]) == 2
    assert len(result["tts"]) == 2
    assert len(result["audio"]) == 2
    
    # Check that narrations were extracted correctly
    assert result["tts"][0] == "The day comes to an end"
    assert result["tts"][1] == "As night approaches"

def test_parse_invalid_json():
    """Test handling invalid JSON input"""
    with pytest.raises(Exception):
        parse_detailed_script("This is not JSON")

def test_parse_empty_response():
    """Test handling empty response"""
    with pytest.raises(Exception):
        parse_detailed_script("")

def test_validate_segment_missing_field():
    """Test validation with missing required field"""
    invalid_segment = {
        "start": 0,
        # Missing 'end'
        "narration": "Test narration"
    }
    
    with pytest.raises(ValueError, match="Missing required field: end"):
        validate_segment(invalid_segment)

def test_validate_segment_invalid_timing():
    """Test validation with invalid timing (end <= start)"""
    invalid_segment = {
        "start": 5,
        "end": 5,  # Equal to start
        "narration": "Test narration"
    }
    
    with pytest.raises(ValueError, match="End time must be greater than start time"):
        validate_segment(invalid_segment)

def test_character_face_generation():
    """Test that character faces are generated consistently"""
    segment_with_character = {
        "start": 0,
        "end": 5,
        "narration": "Hello there",
        "image": "John: A tall man with brown hair"
    }
    
    mock_response = json.dumps([segment_with_character])
    result = parse_detailed_script(mock_response)
    
    # Check character face was generated
    assert len(result["image"]) == 1
    assert result["image"][0]["character"] == "John"
    assert "face_prompt" in result["image"][0]
    assert "seed" in result["image"][0]
    
    # Check that the seed is deterministic for the same character
    second_result = parse_detailed_script(mock_response)
    assert result["image"][0]["seed"] == second_result["image"][0]["seed"]
