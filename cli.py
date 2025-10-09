#!/usr/bin/env python3
"""
Command Line Interface for VS Code Project Launcher
Provides CLI access to workspace scanning and launching
"""

import argparse
import sys
import os
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))

from core.workspace_scanner import WorkspaceScanner
from core.launcher import VSCodeLauncher
from core.config_manager import ConfigManager

def list_workspaces(args):
    """List all found workspaces"""
    config_manager = ConfigManager()
    scanner = WorkspaceScanner()
    
    scan_dirs = args.directories or config_manager.config.scan_directories
    recursive = not args.no_recursive
    
    print(f"Scanning directories: {', '.join(scan_dirs)}")
    print(f"Recursive: {recursive}")
    print()
    
    workspaces = scanner.scan_multiple_directories(scan_dirs, recursive)
    
    if not workspaces:
        print("No workspaces found.")
        return
    
    print(f"Found {len(workspaces)} workspace(s):")
    print()
    
    for i, workspace in enumerate(workspaces, 1):
        print(f"{i:2d}. {workspace.name}")
        print(f"     Path: {workspace.full_path}")
        print(f"     Folders: {workspace.folder_count}")
        print(f"     Modified: {workspace.last_modified.strftime('%Y-%m-%d %H:%M')}")
        if args.verbose:
            for folder in workspace.folders:
                print(f"       - {folder}")
        print()

def launch_workspace(args):
    """Launch a specific workspace"""
    launcher = VSCodeLauncher()
    
    if not launcher.is_available:
        print("Error: VS Code not found. Make sure it's installed and in PATH.")
        sys.exit(1)
    
    workspace_path = args.workspace
    
    # If it's a number, treat as index from list
    if workspace_path.isdigit():
        config_manager = ConfigManager()
        scanner = WorkspaceScanner()
        
        workspaces = scanner.scan_multiple_directories(
            config_manager.config.scan_directories,
            config_manager.config.recursive_scan
        )
        
        index = int(workspace_path) - 1
        if 0 <= index < len(workspaces):
            workspace_path = workspaces[index].full_path
        else:
            print(f"Error: Invalid workspace index {workspace_path}")
            sys.exit(1)
    
    # Expand path
    workspace_path = os.path.expanduser(workspace_path)
    
    if not os.path.exists(workspace_path):
        print(f"Error: Workspace file not found: {workspace_path}")
        sys.exit(1)
    
    print(f"Launching workspace: {workspace_path}")
    
    if launcher.launch_workspace(workspace_path, args.new_window):
        # Add to recent workspaces
        config_manager = ConfigManager()
        config_manager.add_recent_workspace(workspace_path)
        print("Workspace launched successfully.")
    else:
        print("Error: Failed to launch workspace.")
        sys.exit(1)

def search_workspaces(args):
    """Search for workspaces by name"""
    config_manager = ConfigManager()
    scanner = WorkspaceScanner()
    
    workspaces = scanner.scan_multiple_directories(
        config_manager.config.scan_directories,
        config_manager.config.recursive_scan
    )
    
    query = args.query.lower()
    matches = []
    
    for workspace in workspaces:
        if query in workspace.name.lower() or query in workspace.path.lower():
            matches.append(workspace)
    
    if not matches:
        print(f"No workspaces found matching '{args.query}'")
        return
    
    print(f"Found {len(matches)} workspace(s) matching '{args.query}':")
    print()
    
    for i, workspace in enumerate(matches, 1):
        print(f"{i:2d}. {workspace.name}")
        print(f"     Path: {workspace.full_path}")
        print()

def show_favorites(args):
    """Show favorite workspaces"""
    config_manager = ConfigManager()
    scanner = WorkspaceScanner()
    
    favorites = config_manager.config.favorites
    
    if not favorites:
        print("No favorite workspaces configured.")
        return
    
    print(f"Favorite workspaces ({len(favorites)}):")
    print()
    
    for i, fav_path in enumerate(favorites, 1):
        workspace = scanner.get_workspace_by_path(fav_path)
        if workspace:
            print(f"{i:2d}. {workspace.name}")
            print(f"     Path: {workspace.full_path}")
        else:
            print(f"{i:2d}. [Not Found]")
            print(f"     Path: {fav_path}")
        print()

def show_recent(args):
    """Show recent workspaces"""
    config_manager = ConfigManager()
    scanner = WorkspaceScanner()
    
    recent = config_manager.config.recent_workspaces
    
    if not recent:
        print("No recent workspaces.")
        return
    
    print(f"Recent workspaces ({len(recent)}):")
    print()
    
    for i, recent_path in enumerate(recent, 1):
        workspace = scanner.get_workspace_by_path(recent_path)
        if workspace:
            print(f"{i:2d}. {workspace.name}")
            print(f"     Path: {workspace.full_path}")
            print(f"     Modified: {workspace.last_modified.strftime('%Y-%m-%d %H:%M')}")
        else:
            print(f"{i:2d}. [Not Found]")
            print(f"     Path: {recent_path}")
        print()

def show_config(args):
    """Show current configuration"""
    config_manager = ConfigManager()
    config = config_manager.config
    
    print("Current Configuration:")
    print(f"  Config file: {config_manager.config_file}")
    print()
    print("Scan Directories:")
    for directory in config.scan_directories:
        print(f"  - {directory}")
    print()
    print(f"Recursive scan: {config.recursive_scan}")
    print(f"Auto scan on startup: {config.auto_scan}")
    print(f"Show folder count: {config.show_folder_count}")
    print(f"Max recent workspaces: {config.max_recent}")
    print(f"Theme: {config.theme}")
    print()
    print(f"Favorites: {len(config.favorites)}")
    print(f"Recent workspaces: {len(config.recent_workspaces)}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='VS Code Project Launcher CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                          # List all workspaces
  %(prog)s list -d ~/dev ~/projects      # List workspaces in specific directories
  %(prog)s launch 1                      # Launch first workspace from list
  %(prog)s launch ~/project.code-workspace  # Launch specific workspace
  %(prog)s search "my project"           # Search for workspaces
  %(prog)s favorites                     # Show favorite workspaces
  %(prog)s recent                        # Show recent workspaces
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List workspaces')
    list_parser.add_argument('-d', '--directories', nargs='+', help='Directories to scan')
    list_parser.add_argument('--no-recursive', action='store_true', help='Disable recursive scanning')
    list_parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed information')
    list_parser.set_defaults(func=list_workspaces)
    
    # Launch command
    launch_parser = subparsers.add_parser('launch', help='Launch workspace')
    launch_parser.add_argument('workspace', help='Workspace file path or index from list')
    launch_parser.add_argument('-n', '--new-window', action='store_true', help='Open in new window')
    launch_parser.set_defaults(func=launch_workspace)
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search workspaces')
    search_parser.add_argument('query', help='Search query')
    search_parser.set_defaults(func=search_workspaces)
    
    # Favorites command
    favorites_parser = subparsers.add_parser('favorites', help='Show favorite workspaces')
    favorites_parser.set_defaults(func=show_favorites)
    
    # Recent command
    recent_parser = subparsers.add_parser('recent', help='Show recent workspaces')
    recent_parser.set_defaults(func=show_recent)
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Show configuration')
    config_parser.set_defaults(func=show_config)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()