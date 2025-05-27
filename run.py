#!/usr/bin/env python
"""
VidGen Application Launcher

This script is the main entry point to run the VidGen application.
"""
import sys
import os
import argparse
import logging

# Add the src directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from vidgen.main import demo
from vidgen.utils.logging_config import configure_logging

def main():
    """Main entry point with command line argument handling"""
    parser = argparse.ArgumentParser(description="VidGen - Video Generator from Scene Scripts")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the Gradio interface on")
    parser.add_argument("--share", action="store_true", help="Create a shareable link")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--log-to-file", action="store_true", help="Log to file")
    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logger = configure_logging(log_to_file=args.log_to_file)
    logger.setLevel(log_level)
    
    logger.info("Starting VidGen application")
    
    # Launch the Gradio interface
    demo.launch(
        server_port=args.port,
        share=args.share,
        debug=args.debug
    )
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
