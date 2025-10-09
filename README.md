# VS Code Project Launcher

<div align="center">

![VS Code Project Launcher](https://img.shields.io/badge/VS%20Code-Project%20Launcher-007ACC?style=for-the-badge&logo=visual-studio-code)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A desktop application to easily manage and launch VS Code workspaces from a centralized interface.

[Installation](#installation) •
[Features](#features) •
[Usage](#usage) •
[Contributing](#contributing)

</div>

## 🚀 Features

- **Workspace Discovery**: Automatically scans your development directories for `.code-workspace` files
- **Quick Launch**: Double-click to open workspaces in VS Code
- **Search & Filter**: Find workspaces quickly by name or path
- **Favorites**: Mark frequently used workspaces as favorites
- **Recent Workspaces**: Keep track of recently opened workspaces
- **Desktop Integration**: Install as a desktop application on Linux
- **Configurable**: Set custom scan directories and preferences

## 📸 Screenshots

![Main Window](https://via.placeholder.com/600x400?text=Main+Window+Screenshot)
*Main application window showing workspace list with search and favorites*

![Settings Dialog](https://via.placeholder.com/400x300?text=Settings+Dialog)
*Configuration dialog for scan directories and preferences*

## 🛠 Installation

### Prerequisites

- Python 3.7+
- VS Code installed and accessible via `code` command
- Linux desktop environment (tested on Fedora, Ubuntu, etc.)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Zajfan/vscode-project-launcher.git
cd vscode-project-launcher

# Run the setup script
./setup_launcher.sh

# Launch the application
./launch.sh
```

### Manual Installation

```bash
# Install system dependencies (Fedora/RHEL)
sudo dnf install python3-tkinter

# Install Python dependencies
pip3 install --user -r requirements.txt

# Make scripts executable
chmod +x launch.sh cli.py src/install_desktop.py
```

### Desktop Integration

```bash
# Install desktop shortcut and menu entry
python3 src/install_desktop.py --desktop-shortcut

# System-wide installation (requires sudo)
sudo python3 src/install_desktop.py --system --desktop-shortcut
```

## 📚 Usage

### GUI Mode (Recommended)

Launch the graphical interface:
```bash
./launch.sh
```

### Command Line Interface

```bash
# List all workspaces
./cli.py list

# Search for workspaces
./cli.py search "project name"

# Launch a workspace by index
./cli.py launch 1

# Launch a specific workspace file
./cli.py launch ~/path/to/workspace.code-workspace

# Show favorites and recent workspaces
./cli.py favorites
./cli.py recent
```

### Keyboard Shortcuts

- `Ctrl+R` or `F5`: Refresh workspace list
- `Ctrl+F`: Focus search box
- `Ctrl+O` or `Enter`: Open selected workspace
- `Ctrl+N`: Open workspace in new window
- `Escape`: Clear search

## 🏗 Project Structure
```
src/
├── main.py              # Application entry point
├── gui/                 # GUI components
│   ├── __init__.py
│   ├── main_window.py   # Main application window
│   ├── settings_dialog.py # Settings configuration
│   └── workspace_item.py # Workspace list item widget
├── core/                # Core functionality
│   ├── __init__.py
│   ├── workspace_scanner.py # Workspace file discovery
│   ├── config_manager.py    # Configuration management
│   └── launcher.py          # VS Code launching logic
└── utils/               # Utility functions
    ├── __init__.py
    └── file_utils.py    # File system utilities
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/vscode-project-launcher.git
cd vscode-project-launcher

# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
./launch.sh
```

### Areas for Contribution

- 🐛 **Bug Reports**: Found a bug? Please open an issue
- 💡 **Feature Requests**: Have an idea? Let's discuss it
- 📖 **Documentation**: Help improve the docs
- 🧪 **Testing**: Add unit tests and integration tests
- 🎨 **UI/UX**: Improve the interface design
- 🚀 **Performance**: Optimize scanning and launching

## 🐛 Troubleshooting

### Common Issues

**VS Code not found**
```bash
# Install the 'code' command in VS Code
# Ctrl+Shift+P → "Shell Command: Install 'code' command in PATH"
```

**Permission errors when scanning**
```bash
# Check directory permissions
ls -la /path/to/directory
```

**Missing tkinter**
```bash
# Fedora/RHEL/CentOS
sudo dnf install python3-tkinter

# Ubuntu/Debian
sudo apt install python3-tk
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- VS Code team for creating an amazing editor
- Python tkinter community for GUI framework
- All contributors who help improve this project

## ⭐ Support

If you found this project helpful, please consider:
- ⭐ **Starring** the repository
- 🐛 **Reporting** bugs and issues
- 💡 **Suggesting** new features
- 🤝 **Contributing** code or documentation

---

<div align="center">
Made with ❤️ for the VS Code community
</div>