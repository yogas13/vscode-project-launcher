#!/bin/bash
# Setup script for VS Code Project Launcher
# Installs dependencies and sets up the application

set -e

echo "=== VS Code Project Launcher Setup ==="
echo

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if tkinter is available
echo
echo "Checking tkinter availability..."
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✓ tkinter is available"
else
    echo "✗ tkinter not found"
    echo "  Please install tkinter for your distribution:"
    echo "  - Fedora/RHEL/CentOS: sudo dnf install python3-tkinter"
    echo "  - Ubuntu/Debian: sudo apt install python3-tk"
    echo "  - Arch Linux: sudo pacman -S tk"
    echo "  - openSUSE: sudo zypper install python3-tk"
    echo
    echo "After installing tkinter, run this script again."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "Error: pip is required but not installed."
    echo "Please install pip and try again."
    exit 1
fi

echo "✓ pip found"

# Install Python dependencies
echo
echo "Installing Python dependencies..."

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found"
    exit 1
fi

# Install base requirements
pip3 install --user -r requirements.txt

# Install optional dependencies for enhanced features
echo
echo "Installing optional dependencies for enhanced features..."

# System tray support
echo "- Installing pystray for system tray support..."
pip3 install --user pystray || echo "  Warning: Could not install pystray (system tray will be disabled)"

# Better file watching
echo "- Installing watchdog for file monitoring..."
pip3 install --user watchdog || echo "  Warning: Could not install watchdog"

echo
echo "✓ Dependencies installed"

# Make scripts executable
echo
echo "Making scripts executable..."
chmod +x launch.sh
chmod +x cli.py
chmod +x src/install_desktop.py
echo "✓ Scripts made executable"

# Test the application
echo
echo "Testing application..."
if python3 -c "import sys; sys.path.insert(0, 'src'); from core.config_manager import ConfigManager; print('✓ Core modules import successfully')"; then
    echo "✓ Application modules load correctly"
else
    echo "✗ Error loading application modules"
    exit 1
fi

# Check VS Code installation
echo
echo "Checking VS Code installation..."
if command -v code &> /dev/null; then
    echo "✓ VS Code found: $(code --version | head -n1)"
elif command -v code-insiders &> /dev/null; then
    echo "✓ VS Code Insiders found"
elif command -v codium &> /dev/null; then
    echo "✓ VSCodium found"
else
    echo "⚠ Warning: VS Code not found in PATH"
    echo "  Please make sure VS Code is installed and the 'code' command is available"
    echo "  You can install the 'code' command from VS Code: Ctrl+Shift+P > 'Shell Command: Install code command in PATH'"
fi

echo
echo "=== Setup Complete ==="
echo
echo "You can now run the VS Code Project Launcher:"
echo "  GUI:  ./launch.sh"
echo "  CLI:  ./cli.py list"
echo
echo "To install desktop integration:"
echo "  python3 src/install_desktop.py --desktop-shortcut"
echo
echo "For system-wide installation (requires sudo):"
echo "  sudo python3 src/install_desktop.py --system --desktop-shortcut"
echo