"""
VidGen utilities

This package contains utility functions and helpers:
- File management utilities
- Logging configuration
- General helper functions
"""

from vidgen.utils.file_manager import (
    get_temp_dir,
    get_output_dir,
    generate_unique_filename,
    register_temp_file,
    cleanup_temp_files
)

from vidgen.utils.logging_config import configure_logging
from vidgen.utils.helpers import (
    create_deterministic_seed,
    ensure_dirs,
    load_json_safe,
    format_time
)
