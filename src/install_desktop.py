#!/usr/bin/env python3
"""
Desktop Integration Installer
Creates desktop shortcuts and menu entries for the VS Code Project Launcher
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def get_app_info():
    """Get application information"""
    app_dir = Path(__file__).parent
    return {
        'name': 'VS Code Project Launcher',
        'description': 'Manage and launch VS Code workspaces',
        'executable': app_dir / 'main.py',
        'icon_path': app_dir / 'assets' / 'icon.png',
        'app_dir': app_dir
    }

def create_desktop_file(app_info):
    """Create .desktop file content"""
    executable = str(app_info['executable'])
    icon_path = str(app_info['icon_path']) if app_info['icon_path'].exists() else 'code'
    
    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={app_info['name']}
Comment={app_info['description']}
Icon={icon_path}
Exec=python3 "{executable}"
Terminal=false
Categories=Development;IDE;
Keywords=vscode;workspace;project;launcher;
StartupNotify=true
StartupWMClass=VSCodeProjectLauncher
"""
    return desktop_content

def install_desktop_file(app_info, system_wide=False):
    """Install desktop file"""
    desktop_content = create_desktop_file(app_info)
    
    if system_wide:
        # System-wide installation
        desktop_dir = Path('/usr/share/applications')
        if not desktop_dir.exists() or not os.access(desktop_dir, os.W_OK):
            print("Error: Cannot write to system applications directory. Try running with sudo or install for user only.")
            return False
    else:
        # User installation
        desktop_dir = Path.home() / '.local' / 'share' / 'applications'
        desktop_dir.mkdir(parents=True, exist_ok=True)
    
    desktop_file_path = desktop_dir / 'vscode-project-launcher.desktop'
    
    try:
        with open(desktop_file_path, 'w') as f:
            f.write(desktop_content)
        
        # Make desktop file executable
        os.chmod(desktop_file_path, 0o755)
        
        print(f"Desktop file installed: {desktop_file_path}")
        return True
        
    except Exception as e:
        print(f"Error installing desktop file: {e}")
        return False

def create_desktop_shortcut(app_info):
    """Create desktop shortcut"""
    desktop_dir = Path.home() / 'Desktop'
    if not desktop_dir.exists():
        return False
    
    desktop_file_path = desktop_dir / 'VSCode Project Launcher.desktop'
    desktop_content = create_desktop_file(app_info)
    
    try:
        with open(desktop_file_path, 'w') as f:
            f.write(desktop_content)
        
        # Make desktop file executable
        os.chmod(desktop_file_path, 0o755)
        
        print(f"Desktop shortcut created: {desktop_file_path}")
        return True
        
    except Exception as e:
        print(f"Error creating desktop shortcut: {e}")
        return False

def create_application_icon(app_info):
    """Create or copy application icon"""
    icon_dir = app_info['app_dir'] / 'assets'
    icon_dir.mkdir(exist_ok=True)
    
    icon_path = icon_dir / 'icon.png'
    
    if icon_path.exists():
        return True
    
    # Try to create a simple icon using Python's PIL if available
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple icon
        size = 128
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw background circle
        circle_color = (0, 122, 204)  # VS Code blue
        draw.ellipse([10, 10, size-10, size-10], fill=circle_color)
        
        # Draw VS Code-like icon
        # Draw bracket-like shapes
        white = (255, 255, 255)
        draw.rectangle([25, 35, 35, 95], fill=white)
        draw.rectangle([25, 35, 60, 45], fill=white)
        draw.rectangle([25, 85, 60, 95], fill=white)
        
        draw.rectangle([95, 35, 105, 95], fill=white)
        draw.rectangle([70, 35, 105, 45], fill=white)
        draw.rectangle([70, 85, 105, 95], fill=white)
        
        # Save icon
        img.save(icon_path, 'PNG')
        print(f"Created application icon: {icon_path}")
        return True
        
    except ImportError:
        print("PIL not available, skipping icon creation")
        return False
    except Exception as e:
        print(f"Error creating icon: {e}")
        return False

def update_desktop_database():
    """Update desktop database"""
    try:
        subprocess.run(['update-desktop-database', str(Path.home() / '.local' / 'share' / 'applications')], 
                      check=True, capture_output=True)
        print("Desktop database updated")
        return True
    except subprocess.CalledProcessError:
        print("Warning: Could not update desktop database")
        return False
    except FileNotFoundError:
        print("update-desktop-database not found, skipping")
        return False

def create_launcher_script():
    """Create a launcher script in user's local bin"""
    app_info = get_app_info()
    bin_dir = Path.home() / '.local' / 'bin'
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    launcher_path = bin_dir / 'vscode-project-launcher'
    
    launcher_content = f"""#!/bin/bash
# VS Code Project Launcher
cd "{app_info['app_dir']}"
python3 "{app_info['executable']}" "$@"
"""
    
    try:
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        os.chmod(launcher_path, 0o755)
        print(f"Launcher script created: {launcher_path}")
        
        # Check if ~/.local/bin is in PATH
        user_path = os.environ.get('PATH', '')
        if str(bin_dir) not in user_path:
            print(f"\nNote: Add {bin_dir} to your PATH to use 'vscode-project-launcher' command")
            print(f"Add this line to your ~/.bashrc or ~/.zshrc:")
            print(f"export PATH=\"$PATH:{bin_dir}\"")
        
        return True
        
    except Exception as e:
        print(f"Error creating launcher script: {e}")
        return False

def install(system_wide=False, desktop_shortcut=False):
    """Main installation function"""
    print("Installing VS Code Project Launcher...")
    
    app_info = get_app_info()
    
    # Check if main script exists
    if not app_info['executable'].exists():
        print(f"Error: Main script not found at {app_info['executable']}")
        return False
    
    success = True
    
    # Create application icon
    create_application_icon(app_info)
    
    # Install desktop file
    if not install_desktop_file(app_info, system_wide):
        success = False
    
    # Create desktop shortcut if requested
    if desktop_shortcut:
        if not create_desktop_shortcut(app_info):
            success = False
    
    # Create launcher script
    if not create_launcher_script():
        success = False
    
    # Update desktop database
    update_desktop_database()
    
    if success:
        print("\nInstallation completed successfully!")
        print("\nYou can now:")
        print("1. Find 'VS Code Project Launcher' in your application menu")
        print("2. Run 'vscode-project-launcher' from terminal (if ~/.local/bin is in PATH)")
        if desktop_shortcut:
            print("3. Use the desktop shortcut")
        
        print("\nTo uninstall, run: python3 install_desktop.py --uninstall")
    else:
        print("\nInstallation completed with some errors.")
    
    return success

def uninstall():
    """Uninstall desktop integration"""
    print("Uninstalling VS Code Project Launcher...")
    
    removed_files = []
    
    # Remove desktop file
    desktop_dirs = [
        Path.home() / '.local' / 'share' / 'applications',
        Path('/usr/share/applications')
    ]
    
    for desktop_dir in desktop_dirs:
        desktop_file = desktop_dir / 'vscode-project-launcher.desktop'
        if desktop_file.exists():
            try:
                desktop_file.unlink()
                removed_files.append(str(desktop_file))
            except Exception as e:
                print(f"Error removing {desktop_file}: {e}")
    
    # Remove desktop shortcut
    desktop_shortcut = Path.home() / 'Desktop' / 'VSCode Project Launcher.desktop'
    if desktop_shortcut.exists():
        try:
            desktop_shortcut.unlink()
            removed_files.append(str(desktop_shortcut))
        except Exception as e:
            print(f"Error removing desktop shortcut: {e}")
    
    # Remove launcher script
    launcher_script = Path.home() / '.local' / 'bin' / 'vscode-project-launcher'
    if launcher_script.exists():
        try:
            launcher_script.unlink()
            removed_files.append(str(launcher_script))
        except Exception as e:
            print(f"Error removing launcher script: {e}")
    
    # Update desktop database
    update_desktop_database()
    
    if removed_files:
        print("Removed files:")
        for file_path in removed_files:
            print(f"  - {file_path}")
    else:
        print("No files found to remove.")
    
    print("Uninstallation completed.")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Install desktop integration for VS Code Project Launcher')
    parser.add_argument('--system', action='store_true', help='Install system-wide (requires sudo)')
    parser.add_argument('--desktop-shortcut', action='store_true', help='Create desktop shortcut')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall desktop integration')
    
    args = parser.parse_args()
    
    if args.uninstall:
        uninstall()
    else:
        install(system_wide=args.system, desktop_shortcut=args.desktop_shortcut)

if __name__ == '__main__':
    main()