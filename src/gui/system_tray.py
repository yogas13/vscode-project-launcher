#!/usr/bin/env python3
"""
System Tray Integration
Provides system tray functionality for quick workspace access
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
from typing import List, Optional, Callable
import subprocess
import os

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

from core.workspace_scanner import WorkspaceScanner, WorkspaceInfo
from core.launcher import VSCodeLauncher
from core.config_manager import ConfigManager

class SystemTrayManager:
    """Manages system tray integration"""
    
    def __init__(self, config_manager: ConfigManager, show_main_window_callback: Callable):
        self.config_manager = config_manager
        self.show_main_window = show_main_window_callback
        self.workspace_scanner = WorkspaceScanner()
        self.vscode_launcher = VSCodeLauncher()
        
        self.icon = None
        self.workspaces: List[WorkspaceInfo] = []
        self.favorites: List[WorkspaceInfo] = []
        
        # Load initial workspaces
        self._load_workspaces()
    
    def _create_icon_image(self):
        """Create system tray icon"""
        try:
            # Try to load custom icon first
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.png')
            if os.path.exists(icon_path):
                return Image.open(icon_path)
        except Exception:
            pass
        
        # Create simple icon programmatically
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # VS Code-like icon
        color = (0, 122, 204)  # VS Code blue
        draw.ellipse([8, 8, size-8, size-8], fill=color)
        
        # Simple bracket shapes
        white = (255, 255, 255)
        draw.rectangle([16, 20, 20, 44], fill=white)
        draw.rectangle([16, 20, 32, 24], fill=white)
        draw.rectangle([16, 40, 32, 44], fill=white)
        
        draw.rectangle([44, 20, 48, 44], fill=white)
        draw.rectangle([32, 20, 48, 24], fill=white)
        draw.rectangle([32, 40, 48, 44], fill=white)
        
        return image
    
    def _load_workspaces(self):
        """Load workspaces in background"""
        def load_thread():
            try:
                scan_dirs = self.config_manager.config.scan_directories
                recursive = self.config_manager.config.recursive_scan
                
                self.workspaces = self.workspace_scanner.scan_multiple_directories(scan_dirs, recursive)
                
                # Filter favorites
                self.favorites = [
                    ws for ws in self.workspaces 
                    if self.config_manager.is_favorite(ws.full_path)
                ]
                
                # Update menu if icon exists
                if self.icon:
                    self.icon.menu = self._create_menu()
                    
            except Exception as e:
                print(f"Error loading workspaces: {e}")
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def _create_menu(self):
        """Create system tray menu"""
        menu_items = []
        
        # Show main window
        menu_items.append(pystray.MenuItem("Show Launcher", self.show_main_window))
        menu_items.append(pystray.Menu.SEPARATOR)
        
        # Recent workspaces
        recent_workspaces = self.config_manager.config.recent_workspaces[:5]
        if recent_workspaces:
            recent_items = []
            for workspace_path in recent_workspaces:
                # Find workspace info
                workspace = self.workspace_scanner.get_workspace_by_path(workspace_path)
                if workspace:
                    recent_items.append(
                        pystray.MenuItem(
                            workspace.name,
                            lambda _, ws_path=workspace_path: self._launch_workspace(ws_path)
                        )
                    )
            
            if recent_items:
                menu_items.append(pystray.MenuItem("Recent", pystray.Menu(*recent_items)))
                menu_items.append(pystray.Menu.SEPARATOR)
        
        # Favorites
        if self.favorites:
            favorite_items = []
            for workspace in self.favorites[:10]:  # Limit to 10 favorites
                favorite_items.append(
                    pystray.MenuItem(
                        f"★ {workspace.name}",
                        lambda _, ws_path=workspace.full_path: self._launch_workspace(ws_path)
                    )
                )
            
            menu_items.append(pystray.MenuItem("Favorites", pystray.Menu(*favorite_items)))
            menu_items.append(pystray.Menu.SEPARATOR)
        
        # Actions
        menu_items.append(pystray.MenuItem("Refresh", self._refresh_workspaces))
        menu_items.append(pystray.Menu.SEPARATOR)
        menu_items.append(pystray.MenuItem("Quit", self._quit_application))
        
        return pystray.Menu(*menu_items)
    
    def _launch_workspace(self, workspace_path: str):
        """Launch workspace from tray"""
        if self.vscode_launcher.launch_workspace(workspace_path):
            self.config_manager.add_recent_workspace(workspace_path)
    
    def _refresh_workspaces(self):
        """Refresh workspace list"""
        self.workspace_scanner.clear_cache()
        self._load_workspaces()
    
    def _quit_application(self):
        """Quit the application"""
        if self.icon:
            self.icon.stop()
    
    def start_tray(self):
        """Start system tray"""
        if not TRAY_AVAILABLE:
            print("System tray not available (pystray not installed)")
            return False
        
        try:
            image = self._create_icon_image()
            menu = self._create_menu()
            
            self.icon = pystray.Icon(
                "vscode-launcher",
                image,
                "VS Code Project Launcher",
                menu
            )
            
            # Run in separate thread
            def run_tray():
                self.icon.run()
            
            threading.Thread(target=run_tray, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"Error starting system tray: {e}")
            return False
    
    def stop_tray(self):
        """Stop system tray"""
        if self.icon:
            self.icon.stop()
            self.icon = None
    
    def update_menu(self):
        """Update tray menu"""
        if self.icon:
            self.icon.menu = self._create_menu()

class TrayEnabledMainWindow:
    """Main window with system tray support"""
    
    def __init__(self, root: tk.Tk, config_manager: ConfigManager):
        self.root = root
        self.config_manager = config_manager
        self.tray_manager = None
        
        # Check if system tray should be enabled
        self.tray_enabled = getattr(config_manager.config, 'enable_system_tray', True)
        
        if self.tray_enabled and TRAY_AVAILABLE:
            self.tray_manager = SystemTrayManager(config_manager, self._show_from_tray)
            self.tray_manager.start_tray()
        
        # Override window close behavior
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
    
    def _show_from_tray(self):
        """Show window from system tray"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def _on_window_close(self):
        """Handle window close - minimize to tray if enabled"""
        if self.tray_enabled and self.tray_manager:
            # Minimize to tray instead of closing
            self.root.withdraw()
        else:
            # Close normally
            if self.tray_manager:
                self.tray_manager.stop_tray()
            self.root.destroy()
    
    def quit_application(self):
        """Completely quit the application"""
        if self.tray_manager:
            self.tray_manager.stop_tray()
        self.root.destroy()