"""
VidGen model components

This package contains all AI model implementations for:
- Text-to-speech generation
- Image generation 
- Video processing
- Audio generation

Each component is designed to be as independent as possible for maintainability.
"""

from vidgen.models.tts import generate_tts_audio
from vidgen.models.image import generate_character_image
from vidgen.models.video import (
    generate_video_segment, 
    generate_video_with_transitions,
    add_motion_effects,
    create_multi_angle_video,
    concatenate_videos
)
from vidgen.models.audio import generate_background_audio, mix_audio
from vidgen.models.data_models import Character, ScriptSegment, VideoProject
