#!/bin/bash
# Quick launcher script for VS Code Project Launcher

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
APP_DIR="$SCRIPT_DIR/src"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if main.py exists
if [ ! -f "$APP_DIR/main.py" ]; then
    echo "Error: main.py not found in $APP_DIR"
    exit 1
fi

# Launch the application
echo "Starting VS Code Project Launcher..."
cd "$APP_DIR"
python3 main.py "$@"