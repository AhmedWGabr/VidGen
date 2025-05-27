"""
VidGen service components

This package contains business logic services for:
- Script parsing and processing
- Video assembly
- External API integrations (Gemini API)
"""

from vidgen.services.script_parser import parse_detailed_script
from vidgen.services.video_assembler import assemble_video
from vidgen.services.gemini_api import call_gemini_api
