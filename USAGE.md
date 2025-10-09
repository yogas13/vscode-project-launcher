# VS Code Project Launcher - Usage Guide

## Quick Start

### 1. Setup
```bash
# Run the setup script to install dependencies
./setup_launcher.sh

# Or manually install dependencies
pip3 install --user -r requirements.txt
```

### 2. Running the Application

#### GUI Mode (Recommended)
```bash
# Launch the graphical interface
./launch.sh
```

#### CLI Mode
```bash
# List all workspaces
./cli.py list

# Search for workspaces
./cli.py search "project name"

# Launch a workspace by index
./cli.py launch 1

# Launch a specific workspace file
./cli.py launch ~/path/to/workspace.code-workspace

# Show favorites
./cli.py favorites

# Show recent workspaces
./cli.py recent

# Show configuration
./cli.py config
```

### 3. Desktop Integration
```bash
# Install desktop shortcut and menu entry
python3 src/install_desktop.py --desktop-shortcut

# System-wide installation (requires sudo)
sudo python3 src/install_desktop.py --system --desktop-shortcut

# Uninstall desktop integration
python3 src/install_desktop.py --uninstall
```

## Features

### Main Window Features
- **Workspace List**: View all discovered `.code-workspace` files
- **Search & Filter**: Quick search by name or path
- **Favorites**: Mark frequently used workspaces with stars
- **Recent Workspaces**: Track recently opened workspaces
- **Double-click to Launch**: Quick workspace opening
- **Context Menu**: Right-click for additional options

### Configuration Options
- **Scan Directories**: Configure which directories to scan
- **Recursive Scanning**: Enable/disable subdirectory scanning
- **Auto-scan**: Automatically scan on startup
- **Display Settings**: Customize workspace list appearance
- **Recent Limit**: Set maximum number of recent workspaces

### Keyboard Shortcuts
- `Ctrl+R` or `F5`: Refresh workspace list
- `Ctrl+F`: Focus search box
- `Ctrl+O` or `Enter`: Open selected workspace
- `Ctrl+N`: Open workspace in new window
- `Ctrl+Q`: Quit application
- `Escape`: Clear search

### Advanced Features
- **System Tray**: Minimize to system tray (if pystray is installed)
- **Global Hotkeys**: `Ctrl+Alt+V` to show launcher (if pynput is installed)
- **Workspace Metadata**: Shows folder count and last modified date
- **Favorites Management**: Add/remove favorites with right-click
- **Recent Workspace Tracking**: Automatic recent workspace tracking

## Configuration File

The configuration is stored in `~/.config/vscode-launcher/config.json`:

```json
{
  "scan_directories": [
    "/home/user/dev",
    "/home/user/projects"
  ],
  "favorites": [
    "/path/to/favorite.code-workspace"
  ],
  "recent_workspaces": [
    "/path/to/recent.code-workspace"
  ],
  "window_geometry": {
    "width": 800,
    "height": 600,
    "x": 100,
    "y": 100
  },
  "auto_scan": true,
  "max_recent": 10,
  "theme": "default",
  "show_folder_count": true,
  "recursive_scan": true
}
```

## Troubleshooting

### VS Code Not Found
If you get "VS Code not found" errors:
1. Make sure VS Code is installed
2. Install the `code` command: Open VS Code → `Ctrl+Shift+P` → "Shell Command: Install 'code' command in PATH"
3. Or add VS Code to your PATH manually

### Permission Errors
If you get permission errors when scanning:
1. Check directory permissions
2. Make sure you have read access to the directories
3. Some system directories may require elevated permissions

### Missing Dependencies
Install optional dependencies for enhanced features:
```bash
# System tray support
pip3 install --user pystray

# Global hotkeys
pip3 install --user pynput

# File monitoring
pip3 install --user watchdog
```

### Configuration Issues
Reset configuration to defaults:
```bash
./cli.py config  # View current config
# Then manually edit ~/.config/vscode-launcher/config.json
# Or delete the file to reset to defaults
```

## File Structure

```
projectlauncher/
├── src/
│   ├── main.py              # Main application entry point
│   ├── cli.py               # Command-line interface
│   ├── install_desktop.py   # Desktop integration installer
│   ├── core/
│   │   ├── workspace_scanner.py  # Workspace file discovery
│   │   ├── config_manager.py     # Configuration management
│   │   └── launcher.py           # VS Code launching
│   ├── gui/
│   │   ├── main_window.py        # Main GUI window
│   │   ├── settings_dialog.py    # Settings configuration
│   │   └── system_tray.py        # System tray integration
│   └── utils/
│       ├── file_utils.py         # File system utilities
│       └── shortcuts.py          # Keyboard shortcuts
├── launch.sh                # Quick launcher script
├── setup_launcher.sh        # Setup and installation script
├── requirements.txt         # Python dependencies
└── README.md               # Documentation
```

## Tips

1. **Organize Your Workspaces**: Create `.code-workspace` files for your projects to take advantage of VS Code's multi-folder workspaces
2. **Use Favorites**: Mark your most-used workspaces as favorites for quick access
3. **Configure Scan Directories**: Add your common development directories to the scan list
4. **System Tray**: Install pystray to keep the launcher running in the background
5. **Global Hotkey**: Install pynput and use `Ctrl+Alt+V` to quickly show the launcher from anywhere

## Creating Workspace Files

To create a `.code-workspace` file for your project:
1. Open VS Code
2. Open your project folders: File → Add Folder to Workspace
3. Save the workspace: File → Save Workspace As...
4. Choose a location and name (e.g., `myproject.code-workspace`)

The launcher will automatically discover these files when scanning.