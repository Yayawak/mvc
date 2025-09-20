import tkinter as tk
from tkinter import ttk, messagebox
from controllers.csv_controllers import ProjectsController
from models.csv_models import Project
from typing import List, Callable, Optional

class ProjectsListView:
    def __init__(self, parent, projects_controller: ProjectsController, 
                 on_project_select: Callable):
        self.parent = parent
        self.projects_controller = projects_controller
        self.on_project_select = on_project_select
        
        self.frame = ttk.Frame(parent)
        self.current_projects: List[Project] = []
        self.setup_ui()
        self.load_projects()
    
    def setup_ui(self):
        # Setup the projects list UI
        # Header frame
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(header_frame, text="CS Camp Projects", 
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Welcome message (no user needed)
        welcome_label = ttk.Label(header_frame, text="Welcome to CS Camp Crowdfunding")
        welcome_label.pack(side=tk.RIGHT)
        
        # Search and filter frame
        filter_frame = ttk.Frame(self.frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Search
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Sort options
        ttk.Label(filter_frame, text="Sort by:").pack(side=tk.LEFT, padx=(20, 5))
        self.sort_var = tk.StringVar(value="newest")
        sort_combo = ttk.Combobox(filter_frame, textvariable=self.sort_var, 
                                 values=["newest", "deadline", "funding"], 
                                 state="readonly", width=15)
        sort_combo.pack(side=tk.LEFT, padx=5)
        sort_combo.bind('<<ComboboxSelected>>', self.on_sort_change)
        
        # Refresh button
        refresh_btn = ttk.Button(filter_frame, text="Refresh", command=self.load_projects)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Projects list frame
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for projects
        columns = ("ID", "Name", "Category", "Target", "Current", "Progress", "Deadline", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.tree.heading("ID", text="Project ID")
        self.tree.heading("Name", text="Project Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Target", text="Target Amount")
        self.tree.heading("Current", text="Current Amount")
        self.tree.heading("Progress", text="Progress %")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Status", text="Status")
        
        # Column widths
        self.tree.column("ID", width=80)
        self.tree.column("Name", width=200)
        self.tree.column("Category", width=100)
        self.tree.column("Target", width=100)
        self.tree.column("Current", width=100)
        self.tree.column("Progress", width=80)
        self.tree.column("Deadline", width=100)
        self.tree.column("Status", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_project_double_click)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def load_projects(self):
        # Load projects from database
        try:
            self.status_var.set("Loading projects...")
            self.frame.update()
            
            # Get projects based on current sort
            sort_by = self.sort_var.get()
            self.current_projects = self.projects_controller.get_projects_sorted(sort_by)
            
            # Apply search filter if any
            search_term = self.search_var.get().strip()
            if search_term:
                self.current_projects = [p for p in self.current_projects 
                                       if search_term.lower() in p.name.lower()]
            
            self.populate_tree()
            self.status_var.set(f"Loaded {len(self.current_projects)} projects")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load projects: {str(e)}")
            self.status_var.set("Error loading projects")
    
    def populate_tree(self):
        # Populate the treeview with projects
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add projects
        for project in self.current_projects:
            # Get category name from category_id
            category_name = self.projects_controller.get_category_name(project.category_id)
            status = "Active" if project.is_active else "Expired"
            
            self.tree.insert("", tk.END, values=(
                project.id,
                project.name,
                category_name,
                f"${project.target_amount:,.2f}",
                f"${project.current_amount:,.2f}",
                f"{project.progress_percentage:.1f}%",
                project.deadline.strftime("%Y-%m-%d"),
                status
            ))
    
    def on_search_change(self, event=None):
        # Handle search text change
        self.load_projects()
    
    def on_sort_change(self, event=None):
        # Handle sort option change
        self.load_projects()
    
    def on_project_double_click(self, event):
        # Handle double-click on project
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            project_id = item['values'][0]
            self.on_project_select(project_id)
    
    def show(self):
        # Show the projects list view
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.load_projects()
    
    def hide(self):
        # Hide the projects list view
        self.frame.pack_forget()
