"""
Main Window
The primary GUI interface for the VS Code Project Launcher
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from typing import List, Optional
from pathlib import Path

from core.workspace_scanner import WorkspaceScanner, WorkspaceInfo
from core.launcher import VSCodeLauncher
from core.config_manager import ConfigManager
from gui.settings_dialog import SettingsDialog

class MainWindow:
    """Main application window"""
    
    def __init__(self, root: tk.Tk, config_manager: ConfigManager):
        self.root = root
        self.config_manager = config_manager
        self.workspace_scanner = WorkspaceScanner()
        self.vscode_launcher = VSCodeLauncher()
        
        # Application state
        self.workspaces: List[WorkspaceInfo] = []
        self.filtered_workspaces: List[WorkspaceInfo] = []
        self.is_scanning = False
        
        # Setup the main window
        self._setup_window()
        self._create_widgets()
        self._setup_bindings()
        
        # Load workspaces
        self._scan_workspaces()
    
    def _setup_window(self):
        """Configure the main window"""
        self.root.title("VS Code Project Launcher")
        self.root.minsize(600, 400)
        
        # Set window geometry from config
        geometry = self.config_manager.config.window_geometry
        self.root.geometry(f"{geometry['width']}x{geometry['height']}+{geometry['x']}+{geometry['y']}")
        
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def _create_widgets(self):
        """Create and layout all widgets"""
        # Create main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Toolbar
        self._create_toolbar(main_frame)
        
        # Search frame
        self._create_search_frame(main_frame)
        
        # Workspace list
        self._create_workspace_list(main_frame)
        
        # Status bar
        self._create_status_bar(main_frame)
        
    def _create_toolbar(self, parent):
        """Create the toolbar"""
        toolbar = ttk.Frame(parent)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Scan button
        self.scan_button = ttk.Button(
            toolbar, 
            text="Scan Workspaces", 
            command=self._scan_workspaces
        )
        self.scan_button.grid(row=0, column=0, padx=(0, 5))
        
        # Refresh button
        refresh_button = ttk.Button(
            toolbar, 
            text="Refresh", 
            command=self._refresh_workspaces
        )
        refresh_button.grid(row=0, column=1, padx=(0, 5))
        
        # Settings button
        settings_button = ttk.Button(
            toolbar, 
            text="Settings", 
            command=self._open_settings
        )
        settings_button.grid(row=0, column=2, padx=(0, 20))
        
        # VS Code status
        self.vscode_status_label = ttk.Label(
            toolbar, 
            text=f"VS Code: {'Found' if self.vscode_launcher.is_available else 'Not Found'}",
            foreground="green" if self.vscode_launcher.is_available else "red"
        )
        self.vscode_status_label.grid(row=0, column=3, padx=(0, 10))
        
        # Workspace count
        self.count_label = ttk.Label(toolbar, text="Workspaces: 0")
        self.count_label.grid(row=0, column=4)
        
    def _create_search_frame(self, parent):
        """Create the search frame"""
        search_frame = ttk.Frame(parent)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Search label
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_changed)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        
        # Filter options
        self.show_favorites_var = tk.BooleanVar()
        favorites_check = ttk.Checkbutton(
            search_frame, 
            text="Favorites Only", 
            variable=self.show_favorites_var,
            command=self._filter_workspaces
        )
        favorites_check.grid(row=0, column=2, padx=(0, 10))
        
        # Clear search button
        clear_button = ttk.Button(
            search_frame, 
            text="Clear", 
            command=self._clear_search
        )
        clear_button.grid(row=0, column=3)
        
    def _create_workspace_list(self, parent):
        """Create the workspace list"""
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=2, column=0, sticky="nsew")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Create treeview
        columns = ("name", "path", "folders", "modified")
        self.workspace_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Configure columns
        self.workspace_tree.heading("name", text="Workspace Name")
        self.workspace_tree.heading("path", text="Location")
        self.workspace_tree.heading("folders", text="Folders")
        self.workspace_tree.heading("modified", text="Modified")
        
        self.workspace_tree.column("name", width=200, minwidth=150)
        self.workspace_tree.column("path", width=300, minwidth=200)
        self.workspace_tree.column("folders", width=80, minwidth=50)
        self.workspace_tree.column("modified", width=120, minwidth=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.workspace_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.workspace_tree.xview)
        self.workspace_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.workspace_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Context menu
        self._create_context_menu()
        
    def _create_context_menu(self):
        """Create context menu for workspace list"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Open Workspace", command=self._open_selected_workspace)
        self.context_menu.add_command(label="Open in New Window", command=self._open_selected_workspace_new_window)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Add to Favorites", command=self._add_to_favorites)
        self.context_menu.add_command(label="Remove from Favorites", command=self._remove_from_favorites)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Show in File Manager", command=self._show_in_file_manager)
        self.context_menu.add_command(label="Copy Path", command=self._copy_path)
        
    def _create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.grid(row=0, column=0, sticky="w")
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode="indeterminate")
        self.progress.grid(row=0, column=1, sticky="e", padx=(10, 0))
        
    def _setup_bindings(self):
        """Setup event bindings"""
        # Double-click to open workspace
        self.workspace_tree.bind("<Double-1>", lambda e: self._open_selected_workspace())
        
        # Right-click for context menu
        self.workspace_tree.bind("<Button-3>", self._show_context_menu)
        
        # Window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Keyboard shortcuts
        self.root.bind("<Control-r>", lambda e: self._refresh_workspaces())
        self.root.bind("<Control-f>", lambda e: self.search_var.set(""))
        self.root.bind("<Control-o>", lambda e: self._open_selected_workspace())
        
    def _scan_workspaces(self):
        """Scan for workspaces in a background thread"""
        if self.is_scanning:
            return
            
        self.is_scanning = True
        self.scan_button.config(state="disabled")
        self.progress.start()
        self.status_label.config(text="Scanning for workspaces...")
        
        def scan_thread():
            try:
                # Get scan directories from config
                scan_dirs = self.config_manager.config.scan_directories
                recursive = self.config_manager.config.recursive_scan
                
                # Scan for workspaces
                workspaces = self.workspace_scanner.scan_multiple_directories(scan_dirs, recursive)
                
                # Update UI in main thread
                self.root.after(0, self._on_scan_complete, workspaces)
                
            except Exception as e:
                self.root.after(0, self._on_scan_error, str(e))
        
        # Start scan in background thread
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def _on_scan_complete(self, workspaces: List[WorkspaceInfo]):
        """Handle scan completion"""
        self.workspaces = workspaces
        self.filtered_workspaces = workspaces.copy()
        
        self._populate_workspace_list()
        self._update_status(f"Found {len(workspaces)} workspaces")
        
        self.is_scanning = False
        self.scan_button.config(state="normal")
        self.progress.stop()
    
    def _on_scan_error(self, error_message: str):
        """Handle scan error"""
        self._update_status(f"Scan error: {error_message}")
        messagebox.showerror("Scan Error", f"Error scanning for workspaces:\n{error_message}")
        
        self.is_scanning = False
        self.scan_button.config(state="normal")
        self.progress.stop()
    
    def _populate_workspace_list(self):
        """Populate the workspace list with current workspaces"""
        # Clear existing items
        for item in self.workspace_tree.get_children():
            self.workspace_tree.delete(item)
        
        # Add workspaces
        for workspace in self.filtered_workspaces:
            # Add favorite indicator
            name = workspace.name
            if self.config_manager.is_favorite(workspace.full_path):
                name = f"★ {name}"
            
            # Format modified date
            modified = workspace.last_modified.strftime("%Y-%m-%d %H:%M")
            
            # Insert item
            self.workspace_tree.insert(
                "", "end",
                values=(name, workspace.path, workspace.folder_count, modified),
                tags=(workspace.full_path,)
            )
        
        # Update count
        self.count_label.config(text=f"Workspaces: {len(self.filtered_workspaces)}")
    
    def _filter_workspaces(self):
        """Filter workspaces based on search criteria"""
        search_text = self.search_var.get().lower()
        show_favorites_only = self.show_favorites_var.get()
        
        self.filtered_workspaces = []
        
        for workspace in self.workspaces:
            # Check search text
            if search_text and search_text not in workspace.name.lower() and search_text not in workspace.path.lower():
                continue
            
            # Check favorites filter
            if show_favorites_only and not self.config_manager.is_favorite(workspace.full_path):
                continue
            
            self.filtered_workspaces.append(workspace)
        
        self._populate_workspace_list()
    
    def _on_search_changed(self, *args):
        """Handle search text change"""
        self._filter_workspaces()
    
    def _clear_search(self):
        """Clear search and filters"""
        self.search_var.set("")
        self.show_favorites_var.set(False)
        self._filter_workspaces()
    
    def _refresh_workspaces(self):
        """Refresh the workspace list"""
        self.workspace_scanner.clear_cache()
        self._scan_workspaces()
    
    def _get_selected_workspace(self) -> Optional[WorkspaceInfo]:
        """Get the currently selected workspace"""
        selection = self.workspace_tree.selection()
        if not selection:
            return None
        
        item = selection[0]
        workspace_path = self.workspace_tree.item(item)["tags"][0]
        
        # Find workspace by path
        for workspace in self.workspaces:
            if workspace.full_path == workspace_path:
                return workspace
        
        return None
    
    def _open_selected_workspace(self):
        """Open the selected workspace in VS Code"""
        workspace = self._get_selected_workspace()
        if not workspace:
            messagebox.showwarning("No Selection", "Please select a workspace to open.")
            return
        
        if self.vscode_launcher.launch_workspace(workspace.full_path):
            self.config_manager.add_recent_workspace(workspace.full_path)
            self._update_status(f"Opened {workspace.name}")
        else:
            messagebox.showerror("Launch Error", "Failed to launch VS Code. Make sure it's installed and accessible.")
    
    def _open_selected_workspace_new_window(self):
        """Open the selected workspace in a new VS Code window"""
        workspace = self._get_selected_workspace()
        if not workspace:
            return
        
        if self.vscode_launcher.launch_workspace(workspace.full_path, new_window=True):
            self.config_manager.add_recent_workspace(workspace.full_path)
            self._update_status(f"Opened {workspace.name} in new window")
        else:
            messagebox.showerror("Launch Error", "Failed to launch VS Code.")
    
    def _add_to_favorites(self):
        """Add selected workspace to favorites"""
        workspace = self._get_selected_workspace()
        if workspace and self.config_manager.add_favorite(workspace.full_path):
            self._populate_workspace_list()
            self._update_status(f"Added {workspace.name} to favorites")
    
    def _remove_from_favorites(self):
        """Remove selected workspace from favorites"""
        workspace = self._get_selected_workspace()
        if workspace and self.config_manager.remove_favorite(workspace.full_path):
            self._populate_workspace_list()
            self._update_status(f"Removed {workspace.name} from favorites")
    
    def _show_in_file_manager(self):
        """Show selected workspace in file manager"""
        workspace = self._get_selected_workspace()
        if workspace:
            import subprocess
            import os
            subprocess.Popen(['xdg-open', os.path.dirname(workspace.full_path)])
    
    def _copy_path(self):
        """Copy workspace path to clipboard"""
        workspace = self._get_selected_workspace()
        if workspace:
            self.root.clipboard_clear()
            self.root.clipboard_append(workspace.full_path)
            self._update_status(f"Copied path: {workspace.full_path}")
    
    def _show_context_menu(self, event):
        """Show context menu"""
        # Select item under cursor
        item = self.workspace_tree.identify_row(event.y)
        if item:
            self.workspace_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self.root, self.config_manager)
        if dialog.result:
            # Refresh if scan directories changed
            self._scan_workspaces()
    
    def _update_status(self, message: str):
        """Update status bar message"""
        self.status_label.config(text=message)
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _on_closing(self):
        """Handle window closing"""
        # Save window geometry
        geometry = self.root.geometry()
        parts = geometry.split('+')
        size_parts = parts[0].split('x')
        
        if len(parts) >= 3 and len(size_parts) >= 2:
            try:
                width = int(size_parts[0])
                height = int(size_parts[1])
                x = int(parts[1])
                y = int(parts[2])
                self.config_manager.update_window_geometry(width, height, x, y)
            except ValueError:
                pass
        
        self.root.destroy()