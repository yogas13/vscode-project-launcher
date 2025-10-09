"""
Settings Dialog
Configuration dialog for the VS Code Project Launcher
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List
import os

from core.config_manager import ConfigManager

class SettingsDialog:
    """Settings configuration dialog"""
    
    def __init__(self, parent: tk.Tk, config_manager: ConfigManager):
        self.parent = parent
        self.config_manager = config_manager
        self.result = False
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.modal = True
        self.dialog.resizable(True, True)
        self.dialog.geometry("600x500")
        
        # Center the dialog
        self._center_dialog()
        
        # Create widgets
        self._create_widgets()
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def _center_dialog(self):
        """Center dialog relative to parent"""
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (600 // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
    
    def _create_widgets(self):
        """Create and layout all widgets"""
        # Main container
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=(0, 10))
        
        # Scan Directories tab
        self._create_scan_directories_tab(notebook)
        
        # General Settings tab
        self._create_general_settings_tab(notebook)
        
        # Favorites tab
        self._create_favorites_tab(notebook)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Buttons
        ttk.Button(button_frame, text="Cancel", command=self._cancel).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Apply", command=self._apply).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="OK", command=self._ok).pack(side="right")
        
        # Reset button on the left
        ttk.Button(button_frame, text="Reset to Defaults", command=self._reset_defaults).pack(side="left")
    
    def _create_scan_directories_tab(self, notebook):
        """Create scan directories configuration tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Scan Directories")
        
        # Description
        description = ttk.Label(
            frame, 
            text="Configure directories to scan for VS Code workspace files:",
            font=("TkDefaultFont", 10, "bold")
        )
        description.pack(anchor="w", pady=(0, 10))
        
        # Directory list frame
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill="both", expand=True)
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill="both", expand=True, side="left")
        
        self.dir_listbox = tk.Listbox(listbox_frame)
        dir_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.dir_listbox.yview)
        self.dir_listbox.configure(yscrollcommand=dir_scrollbar.set)
        
        self.dir_listbox.pack(side="left", fill="both", expand=True)
        dir_scrollbar.pack(side="right", fill="y")
        
        # Buttons frame
        buttons_frame = ttk.Frame(list_frame)
        buttons_frame.pack(side="right", fill="y", padx=(10, 0))
        
        ttk.Button(buttons_frame, text="Add Directory", command=self._add_directory).pack(fill="x", pady=(0, 5))
        ttk.Button(buttons_frame, text="Remove Selected", command=self._remove_directory).pack(fill="x", pady=(0, 5))
        ttk.Button(buttons_frame, text="Browse", command=self._browse_directory).pack(fill="x", pady=(0, 20))
        
        # Options
        options_frame = ttk.Frame(frame)
        options_frame.pack(fill="x", pady=(10, 0))
        
        self.recursive_var = tk.BooleanVar(value=self.config_manager.config.recursive_scan)
        ttk.Checkbutton(
            options_frame, 
            text="Recursive scan (scan subdirectories)", 
            variable=self.recursive_var
        ).pack(anchor="w")
        
        # Populate directory list
        self._populate_directory_list()
    
    def _create_general_settings_tab(self, notebook):
        """Create general settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="General")
        
        # Auto-scan setting
        auto_frame = ttk.LabelFrame(frame, text="Startup", padding="10")
        auto_frame.pack(fill="x", pady=(0, 10))
        
        self.auto_scan_var = tk.BooleanVar(value=self.config_manager.config.auto_scan)
        ttk.Checkbutton(
            auto_frame, 
            text="Automatically scan for workspaces on startup", 
            variable=self.auto_scan_var
        ).pack(anchor="w")
        
        # Display settings
        display_frame = ttk.LabelFrame(frame, text="Display", padding="10")
        display_frame.pack(fill="x", pady=(0, 10))
        
        self.show_folder_count_var = tk.BooleanVar(value=self.config_manager.config.show_folder_count)
        ttk.Checkbutton(
            display_frame, 
            text="Show folder count in workspace list", 
            variable=self.show_folder_count_var
        ).pack(anchor="w")
        
        # Recent workspaces
        recent_frame = ttk.LabelFrame(frame, text="Recent Workspaces", padding="10")
        recent_frame.pack(fill="x", pady=(0, 10))
        
        recent_control_frame = ttk.Frame(recent_frame)
        recent_control_frame.pack(fill="x")
        
        ttk.Label(recent_control_frame, text="Maximum recent workspaces:").pack(side="left")
        
        self.max_recent_var = tk.StringVar(value=str(self.config_manager.config.max_recent))
        recent_spinner = ttk.Spinbox(
            recent_control_frame, 
            from_=5, to=50, width=10, 
            textvariable=self.max_recent_var
        )
        recent_spinner.pack(side="left", padx=(10, 0))
        
        ttk.Button(
            recent_control_frame, 
            text="Clear Recent", 
            command=self._clear_recent
        ).pack(side="right")
    
    def _create_favorites_tab(self, notebook):
        """Create favorites management tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Favorites")
        
        # Description
        description = ttk.Label(
            frame, 
            text="Manage your favorite workspaces:",
            font=("TkDefaultFont", 10, "bold")
        )
        description.pack(anchor="w", pady=(0, 10))
        
        # Favorites list frame
        fav_list_frame = ttk.Frame(frame)
        fav_list_frame.pack(fill="both", expand=True)
        
        # Listbox with scrollbar
        fav_listbox_frame = ttk.Frame(fav_list_frame)
        fav_listbox_frame.pack(fill="both", expand=True, side="left")
        
        self.fav_listbox = tk.Listbox(fav_listbox_frame)
        fav_scrollbar = ttk.Scrollbar(fav_listbox_frame, orient="vertical", command=self.fav_listbox.yview)
        self.fav_listbox.configure(yscrollcommand=fav_scrollbar.set)
        
        self.fav_listbox.pack(side="left", fill="both", expand=True)
        fav_scrollbar.pack(side="right", fill="y")
        
        # Buttons frame
        fav_buttons_frame = ttk.Frame(fav_list_frame)
        fav_buttons_frame.pack(side="right", fill="y", padx=(10, 0))
        
        ttk.Button(fav_buttons_frame, text="Remove Selected", command=self._remove_favorite).pack(fill="x", pady=(0, 5))
        ttk.Button(fav_buttons_frame, text="Clear All", command=self._clear_favorites).pack(fill="x")
        
        # Populate favorites list
        self._populate_favorites_list()
    
    def _populate_directory_list(self):
        """Populate the scan directories list"""
        self.dir_listbox.delete(0, tk.END)
        for directory in self.config_manager.config.scan_directories:
            self.dir_listbox.insert(tk.END, directory)
    
    def _populate_favorites_list(self):
        """Populate the favorites list"""
        self.fav_listbox.delete(0, tk.END)
        for favorite in self.config_manager.config.favorites:
            # Show just the filename for favorites
            name = os.path.basename(favorite)
            if not name:
                name = favorite
            self.fav_listbox.insert(tk.END, f"{name} ({favorite})")
    
    def _add_directory(self):
        """Add a new scan directory"""
        directory = filedialog.askdirectory(
            title="Select Directory to Scan",
            initialdir=os.path.expanduser("~")
        )
        
        if directory:
            # Check if already in list
            current_dirs = [self.dir_listbox.get(i) for i in range(self.dir_listbox.size())]
            if directory not in current_dirs:
                self.dir_listbox.insert(tk.END, directory)
            else:
                messagebox.showinfo("Directory Already Added", "This directory is already in the scan list.")
    
    def _remove_directory(self):
        """Remove selected scan directory"""
        selection = self.dir_listbox.curselection()
        if selection:
            self.dir_listbox.delete(selection[0])
        else:
            messagebox.showwarning("No Selection", "Please select a directory to remove.")
    
    def _browse_directory(self):
        """Browse and add a directory"""
        self._add_directory()
    
    def _remove_favorite(self):
        """Remove selected favorite"""
        selection = self.fav_listbox.curselection()
        if selection:
            # Get the actual path from the display text
            display_text = self.fav_listbox.get(selection[0])
            # Extract path from "name (path)" format
            if "(" in display_text and display_text.endswith(")"):
                path = display_text[display_text.rfind("(") + 1:-1]
                self.config_manager.remove_favorite(path)
                self._populate_favorites_list()
        else:
            messagebox.showwarning("No Selection", "Please select a favorite to remove.")
    
    def _clear_favorites(self):
        """Clear all favorites"""
        if messagebox.askyesno("Clear Favorites", "Are you sure you want to clear all favorites?"):
            self.config_manager.config.favorites.clear()
            self.config_manager.save_config()
            self._populate_favorites_list()
    
    def _clear_recent(self):
        """Clear recent workspaces"""
        if messagebox.askyesno("Clear Recent", "Are you sure you want to clear the recent workspaces list?"):
            self.config_manager.clear_recent_workspaces()
    
    def _reset_defaults(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            self.config_manager.reset_to_defaults()
            self._update_ui_from_config()
    
    def _update_ui_from_config(self):
        """Update UI elements from current config"""
        self._populate_directory_list()
        self._populate_favorites_list()
        self.recursive_var.set(self.config_manager.config.recursive_scan)
        self.auto_scan_var.set(self.config_manager.config.auto_scan)
        self.show_folder_count_var.set(self.config_manager.config.show_folder_count)
        self.max_recent_var.set(str(self.config_manager.config.max_recent))
    
    def _apply_settings(self):
        """Apply current settings"""
        try:
            # Get scan directories from listbox
            scan_dirs = [self.dir_listbox.get(i) for i in range(self.dir_listbox.size())]
            
            # Validate max_recent value
            try:
                max_recent = int(self.max_recent_var.get())
                if max_recent < 1 or max_recent > 100:
                    raise ValueError("Max recent must be between 1 and 100")
            except ValueError as e:
                messagebox.showerror("Invalid Value", f"Invalid maximum recent value: {e}")
                return False
            
            # Update configuration
            self.config_manager.update_config(
                scan_directories=scan_dirs,
                recursive_scan=self.recursive_var.get(),
                auto_scan=self.auto_scan_var.get(),
                show_folder_count=self.show_folder_count_var.get(),
                max_recent=max_recent
            )
            
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error applying settings: {e}")
            return False
    
    def _ok(self):
        """OK button handler"""
        if self._apply_settings():
            self.result = True
            self.dialog.destroy()
    
    def _apply(self):
        """Apply button handler"""
        if self._apply_settings():
            messagebox.showinfo("Settings Applied", "Settings have been applied successfully.")
    
    def _cancel(self):
        """Cancel button handler"""
        self.result = False
        self.dialog.destroy()