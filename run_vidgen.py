#!/usr/bin/env python
"""
Entry point script for running VidGen with the new package structure.
This simplifies running the application without needing to use the module path.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Import and run the main application
from vidgen.main import demo

if __name__ == "__main__":
    demo.launch()
