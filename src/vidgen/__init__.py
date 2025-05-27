"""
VidGen - Video Generator from Scene Script

This package provides tools and functionality to generate videos from textual scene scripts.

Main components:
    - Script parsing and segmentation
    - Text-to-speech audio generation
    - Image generation for scenes
    - Video assembly and processing
"""

from vidgen.core.config import VideoGenConfig
from vidgen.services.script_parser import parse_detailed_script
from vidgen.services.video_assembler import assemble_video
from vidgen.models.data_models import Character, ScriptSegment, VideoProject
from vidgen.ui.gradio_app import create_gradio_interface

__version__ = '0.1.0'
