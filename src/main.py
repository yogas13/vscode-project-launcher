#!/usr/bin/env python3
"""
VS Code Project Launcher
A desktop application to manage and launch VS Code workspaces
"""

import sys
import os
import tkinter as tk
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from gui.main_window import MainWindow
from core.config_manager import ConfigManager

def main():
    """Main application entry point"""
    try:
        # Initialize configuration
        config_manager = ConfigManager()
        
        # Create and run the GUI application
        root = tk.Tk()
        app = MainWindow(root, config_manager)
        
        # Center the window on screen
        app.center_window()
        
        # Start the main loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()