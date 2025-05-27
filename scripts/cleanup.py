#!/usr/bin/env python
"""
Script to clean up temporary files and caches in the VidGen project.
"""

import os
import sys
import shutil
import logging
from pathlib import Path
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('cleanup')

# Root directory (parent of script directory)
ROOT_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def cleanup_temp_files():
    """Clean up temporary files in the output directories."""
    try:
        temp_dir = ROOT_DIR / "outputs" / "temp"
        if temp_dir.exists():
            logger.info(f"Cleaning temporary files in {temp_dir}")
            for file_path in temp_dir.glob("*"):
                if file_path.is_file():
                    file_path.unlink()
                    logger.debug(f"Deleted: {file_path}")
            logger.info("Temporary files cleaned")
        return True
    except Exception as e:
        logger.error(f"Error cleaning temporary files: {e}")
        return False

def cleanup_pycache():
    """Clean up Python cache files (__pycache__, .pyc, etc.)."""
    try:
        logger.info("Cleaning Python cache files")
        
        # Find and remove __pycache__ directories
        for pycache_dir in ROOT_DIR.glob("**/__pycache__"):
            if pycache_dir.is_dir():
                shutil.rmtree(pycache_dir)
                logger.debug(f"Deleted: {pycache_dir}")
        
        # Find and remove .pyc files
        for pyc_file in ROOT_DIR.glob("**/*.pyc"):
            pyc_file.unlink()
            logger.debug(f"Deleted: {pyc_file}")
        
        # Find and remove .pyo files
        for pyo_file in ROOT_DIR.glob("**/*.pyo"):
            pyo_file.unlink()
            logger.debug(f"Deleted: {pyo_file}")
            
        logger.info("Python cache files cleaned")
        return True
    except Exception as e:
        logger.error(f"Error cleaning Python cache files: {e}")
        return False

def cleanup_all_outputs(confirm=True):
    """Clean up all generated output files (images, videos, audio)."""
    try:
        if confirm:
            response = input("Are you sure you want to delete ALL output files? (yes/no): ")
            if response.lower() not in ["yes", "y"]:
                logger.info("Operation cancelled")
                return False
        
        logger.info("Cleaning all output files")
        
        # Directories to clean
        output_dirs = [
            ROOT_DIR / "outputs" / "videos",
            ROOT_DIR / "outputs" / "images",
            ROOT_DIR / "outputs" / "audio",
            ROOT_DIR / "outputs" / "temp",
        ]
        
        for directory in output_dirs:
            if directory.exists():
                for file_path in directory.glob("*"):
                    if file_path.is_file():
                        file_path.unlink()
                        logger.debug(f"Deleted: {file_path}")
        
        logger.info("All output files cleaned")
        return True
    except Exception as e:
        logger.error(f"Error cleaning output files: {e}")
        return False

def main():
    """Run the cleanup process based on command-line arguments."""
    parser = argparse.ArgumentParser(description="Clean up VidGen project files")
    parser.add_argument("--all", action="store_true", help="Clean all output files (requires confirmation)")
    parser.add_argument("--force", action="store_true", help="Force cleanup without confirmation")
    parser.add_argument("--temp", action="store_true", help="Clean only temporary files")
    parser.add_argument("--cache", action="store_true", help="Clean Python cache files")
    
    args = parser.parse_args()
    
    # Default behavior is to clean temp files and cache
    if not (args.all or args.temp or args.cache):
        args.temp = True
        args.cache = True
    
    if args.temp:
        cleanup_temp_files()
    
    if args.cache:
        cleanup_pycache()
    
    if args.all:
        cleanup_all_outputs(not args.force)
    
    logger.info("Cleanup completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
