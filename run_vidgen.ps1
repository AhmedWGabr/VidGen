# Run VidGen application
# PowerShell script for Windows users
$ErrorActionPreference = "Stop"

# Check if Python is installed
try {
    python --version
}
catch {
    Write-Error "Python is not installed or not in the PATH. Please install Python 3.8 or higher."
    exit 1
}

# Set up the Python path to include the src directory
$env:PYTHONPATH = "$PSScriptRoot\src;$env:PYTHONPATH"

# Run the application
Write-Host "Starting VidGen application..."
python -m src.vidgen.main
