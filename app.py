#!/usr/bin/env python3
"""
CS Camp Crowdfunding System
Main application entry point using CSV files for data storage
No authentication required - simplified version
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.csv_controllers import ProjectsController, StatsController
from views.projects_list_view import ProjectsListView
from views.project_detail_view import ProjectDetailView
from views.stats_view import StatsView
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE

class CrowdfundingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(800, 600)
        
        # Center the window
        self.center_window()
        
        # Initialize controllers (no auth needed)
        self.projects_controller = ProjectsController()
        self.stats_controller = StatsController()
        
        # Initialize views
        self.setup_views()
        
        # Current view
        self.current_view = None
        
        # Show projects list initially (no login required)
        self.show_projects()
    
    def center_window(self):
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_views(self):
        # Setup all views
        # Projects list view (no auth controller needed)
        self.projects_list_view = ProjectsListView(
            self.root,
            self.projects_controller,
            self.on_project_select
        )
        
        # Project detail view (no auth controller needed)
        self.project_detail_view = ProjectDetailView(
            self.root,
            self.projects_controller,
            self.on_back_to_projects
        )
        
        # Statistics view
        self.stats_view = StatsView(
            self.root,
            self.stats_controller,
            self.projects_controller
        )
        
        # Setup main menu
        self.setup_menu()
    
    def setup_menu(self):
        # Setup the main menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Projects", command=self.show_projects)
        file_menu.add_command(label="Statistics", command=self.show_statistics)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def show_projects(self):
        # Show projects list view
        self.hide_current_view()
        self.projects_list_view.show()
        self.current_view = "projects"
    
    def show_project_detail(self, project_id: str):
        # Show project detail view
        self.hide_current_view()
        self.project_detail_view.load_project(project_id)
        self.project_detail_view.show()
        self.current_view = "project_detail"
    
    def show_statistics(self):
        # Show statistics view
        self.hide_current_view()
        self.stats_view.show()
        self.current_view = "statistics"
    
    def hide_current_view(self):
        # Hide the current view
        if self.current_view == "projects":
            self.projects_list_view.hide()
        elif self.current_view == "project_detail":
            self.project_detail_view.hide()
        elif self.current_view == "statistics":
            self.stats_view.hide()
    
    def on_project_select(self, project_id: str):
        # Handle project selection
        self.show_project_detail(project_id)
    
    def on_back_to_projects(self):
        # Handle back to projects
        self.show_projects()
    
    def show_about(self):
        # Show about dialog
        about_text = """
CS Camp Crowdfunding System (CSV Version)
Version 1.0 - No Authentication Required

A crowdfunding platform for CS Camp projects using CSV files for data storage.

Features:
- Project management
- Pledge system with reward tiers
- Statistics and reporting
- CSV-based data storage (no database required)
- No login required - simplified access

Built with Python and Tkinter.
Data stored in CSV files in the 'data' directory.
        """
        messagebox.showinfo("About", about_text)
    
    def run(self):
        # Run the application
        print("CS Camp Crowdfunding System (CSV Version)")
        print("Data stored in CSV files - no database required!")
        print("No authentication required - simplified access!")
        print("Sample data is already loaded in the 'data' directory.")
        
        # Start the GUI
        self.root.mainloop()

def main():
    # Main entry point
    try:
        app = CrowdfundingApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()