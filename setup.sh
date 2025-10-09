#!/bin/bash

# VS Code Project Launcher - Setup Script
# This script helps set up the application and its dependencies

set -e

echo "VS Code Project Launcher Setup"
echo "=============================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or later."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python version: $python_version"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"; then
    echo "Error: Python 3.7 or later is required."
    exit 1
fi

# Check if VS Code is installed
if command -v code &> /dev/null; then
    echo "VS Code found: $(code --version | head -n1)"
elif command -v code-insiders &> /dev/null; then
    echo "VS Code Insiders found: $(code-insiders --version | head -n1)"
elif command -v codium &> /dev/null; then
    echo "VSCodium found: $(codium --version | head -n1)"
else
    echo "Warning: VS Code not found in PATH. The launcher may not work properly."
    echo "Please install VS Code, VS Code Insiders, or VSCodium."
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "Error: pip is not available. Please install pip for Python 3."
    exit 1
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."

if command -v pip3 &> /dev/null; then
    pip3 install --user -r requirements.txt
else
    python3 -m pip install --user -r requirements.txt
fi

echo ""
echo "Testing the application..."

# Test run
if python3 src/main.py --help &> /dev/null; then
    echo "Application test successful!"
else
    echo "Warning: Application test failed. There might be missing dependencies."
fi

echo ""
echo "Setup completed!"
echo ""
echo "To run the application:"
echo "  python3 src/main.py"
echo ""
echo "To install desktop integration:"
echo "  python3 src/install_desktop.py"
echo ""
echo "To install with desktop shortcut:"
echo "  python3 src/install_desktop.py --desktop-shortcut"
echo ""
echo "To uninstall desktop integration:"
echo "  python3 src/install_desktop.py --uninstall"