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

from controllers.csv_controllers import AuthController, ProjectsController, StatsController
from views.login_view import LoginView
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
        
        # Initialize controllers
        self.auth_controller = AuthController()
        self.projects_controller = ProjectsController(self.auth_controller)
        self.stats_controller = StatsController()
        
        # Initialize views
        self.setup_views()
        
        # Current view
        self.current_view = None
        
        # Show login first
        self.show_login()
    
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
        # Login view
        self.login_view = LoginView(
            self.root,
            self.auth_controller,
            self.on_login_success
        )
        
        # Projects list view
        self.projects_list_view = ProjectsListView(
            self.root,
            self.projects_controller,
            self.on_project_select
        )
        
        # Project detail view
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
        
        # Setup status bar
        self.setup_status_bar()
    
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
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # User menu
        user_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="User", menu=user_menu)
        user_menu.add_command(label="Profile", command=self.show_profile)
        user_menu.add_command(label="My Pledges", command=self.show_my_pledges)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Store menubar reference for updates
        self.menubar = menubar
        self.user_menu = user_menu
    
    def setup_status_bar(self):
        # Setup status bar at bottom of window
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_frame, text="Not logged in", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Add logout button to status bar
        self.status_logout_btn = ttk.Button(self.status_frame, text="Logout", command=self.logout)
        self.status_logout_btn.pack(side=tk.RIGHT, padx=5, pady=2)
    
    def show_login(self):
        # Show login view
        self.hide_current_view()
        self.login_view.show()
        self.current_view = "login"
    
    def on_login_success(self):
        # Handle successful login
        self.update_user_display()
        self.show_projects()
    
    def update_user_display(self):
        # Update the window title, menu, and status bar to show current user
        current_user = self.auth_controller.get_current_user()
        if current_user:
            self.root.title(f"{WINDOW_TITLE} - Welcome, {current_user.username}!")
            # Update user menu label
            self.user_menu.entryconfig(0, label=f"Profile ({current_user.username})")
            # Update status bar
            self.status_label.config(text=f"Logged in as: {current_user.username}")
        else:
            self.root.title(WINDOW_TITLE)
            self.status_label.config(text="Not logged in")
    
    def logout(self):
        # Handle logout
        self.auth_controller.logout()
        self.update_user_display()  # This will update title and status bar
        self.show_login()
    
    def show_profile(self):
        # Show user profile (simple message for now)
        current_user = self.auth_controller.get_current_user()
        if current_user:
            messagebox.showinfo("Profile", f"Username: {current_user.username}\nEmail: {current_user.email}\nUser ID: {current_user.id}")
        else:
            messagebox.showerror("Error", "Not logged in")
    
    def show_my_pledges(self):
        # Show user's pledges (simple message for now)
        current_user = self.auth_controller.get_current_user()
        if current_user:
            from repositories.csv_repositories import PledgeRepository
            pledge_repo = PledgeRepository()
            user_pledges = pledge_repo.get_by_user(current_user.id)
            messagebox.showinfo("My Pledges", f"You have made {len(user_pledges)} pledges")
        else:
            messagebox.showerror("Error", "Not logged in")
    
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
        if self.current_view == "login":
            self.login_view.hide()
        elif self.current_view == "projects":
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