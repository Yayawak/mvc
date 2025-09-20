import tkinter as tk
from tkinter import ttk
from controllers.csv_controllers import StatsController, ProjectsController
from typing import Dict, Any, List

class StatsView:
    def __init__(self, parent, stats_controller: StatsController, 
                 projects_controller: ProjectsController):
        self.parent = parent
        self.stats_controller = stats_controller
        self.projects_controller = projects_controller
        
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        self.load_statistics()
    
    def setup_ui(self):
        # Setup the statistics UI
        # Title
        title_label = ttk.Label(self.frame, text="Crowdfunding Statistics", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Main content frame
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Overall statistics frame
        overall_frame = ttk.LabelFrame(main_frame, text="Overall Statistics", padding=10)
        overall_frame.pack(fill=tk.X, pady=10)
        
        # Pledge statistics
        pledge_frame = ttk.Frame(overall_frame)
        pledge_frame.pack(fill=tk.X, pady=5)
        
        self.total_pledges_label = ttk.Label(pledge_frame, text="", font=("Arial", 12))
        self.total_pledges_label.pack(side=tk.LEFT, padx=10)
        
        self.successful_pledges_label = ttk.Label(pledge_frame, text="", 
                                                 font=("Arial", 12), foreground="green")
        self.successful_pledges_label.pack(side=tk.LEFT, padx=10)
        
        self.rejected_pledges_label = ttk.Label(pledge_frame, text="", 
                                               font=("Arial", 12), foreground="red")
        self.rejected_pledges_label.pack(side=tk.LEFT, padx=10)
        
        # Project statistics
        project_frame = ttk.Frame(overall_frame)
        project_frame.pack(fill=tk.X, pady=5)
        
        self.total_projects_label = ttk.Label(project_frame, text="", font=("Arial", 12))
        self.total_projects_label.pack(side=tk.LEFT, padx=10)
        
        self.active_projects_label = ttk.Label(project_frame, text="", 
                                              font=("Arial", 12), foreground="blue")
        self.active_projects_label.pack(side=tk.LEFT, padx=10)
        
        self.completed_projects_label = ttk.Label(project_frame, text="", 
                                                font=("Arial", 12), foreground="orange")
        self.completed_projects_label.pack(side=tk.LEFT, padx=10)
        
        # Funding statistics
        funding_frame = ttk.Frame(overall_frame)
        funding_frame.pack(fill=tk.X, pady=5)
        
        self.total_target_label = ttk.Label(funding_frame, text="", font=("Arial", 12))
        self.total_target_label.pack(side=tk.LEFT, padx=10)
        
        self.total_current_label = ttk.Label(funding_frame, text="", font=("Arial", 12))
        self.total_current_label.pack(side=tk.LEFT, padx=10)
        
        self.overall_progress_label = ttk.Label(funding_frame, text="", 
                                              font=("Arial", 12, "bold"))
        self.overall_progress_label.pack(side=tk.LEFT, padx=10)
        
        # Overall progress bar
        ttk.Label(overall_frame, text="Overall Funding Progress:").pack(anchor=tk.W, pady=(10, 2))
        self.overall_progress_var = tk.DoubleVar()
        self.overall_progress_bar = ttk.Progressbar(overall_frame, variable=self.overall_progress_var, 
                                                  maximum=100, length=400)
        self.overall_progress_bar.pack(anchor=tk.W, pady=2)
        
        # Top projects frame
        top_projects_frame = ttk.LabelFrame(main_frame, text="Top Funded Projects", padding=10)
        top_projects_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview for top projects
        columns = ("Rank", "Project Name", "Current Amount", "Target Amount", "Progress %", "Category")
        self.top_projects_tree = ttk.Treeview(top_projects_frame, columns=columns, show="headings")
        
        # Configure columns
        self.top_projects_tree.heading("Rank", text="Rank")
        self.top_projects_tree.heading("Project Name", text="Project Name")
        self.top_projects_tree.heading("Current Amount", text="Current Amount")
        self.top_projects_tree.heading("Target Amount", text="Target Amount")
        self.top_projects_tree.heading("Progress %", text="Progress %")
        self.top_projects_tree.heading("Category", text="Category")
        
        # Column widths
        self.top_projects_tree.column("Rank", width=50)
        self.top_projects_tree.column("Project Name", width=200)
        self.top_projects_tree.column("Current Amount", width=120)
        self.top_projects_tree.column("Target Amount", width=120)
        self.top_projects_tree.column("Progress %", width=80)
        self.top_projects_tree.column("Category", width=100)
        
        # Scrollbar for top projects
        top_scrollbar = ttk.Scrollbar(top_projects_frame, orient=tk.VERTICAL, 
                                    command=self.top_projects_tree.yview)
        self.top_projects_tree.configure(yscrollcommand=top_scrollbar.set)
        
        # Pack top projects treeview
        self.top_projects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        top_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh button
        refresh_btn = ttk.Button(main_frame, text="Refresh Statistics", command=self.load_statistics)
        refresh_btn.pack(pady=10)
    
    def load_statistics(self):
        # Load and display statistics
        try:
            # Get overall statistics
            overall_stats = self.stats_controller.get_overall_statistics()
            
            # Update pledge statistics
            pledge_stats = overall_stats['pledges']
            self.total_pledges_label.config(text=f"Total Pledges: {pledge_stats['total']}")
            self.successful_pledges_label.config(text=f"Successful: {pledge_stats['successful']}")
            self.rejected_pledges_label.config(text=f"Rejected: {pledge_stats['rejected']}")
            
            # Update project statistics
            project_stats = overall_stats['projects']
            self.total_projects_label.config(text=f"Total Projects: {project_stats['total']}")
            self.active_projects_label.config(text=f"Active: {project_stats['active']}")
            self.completed_projects_label.config(text=f"Completed: {project_stats['completed']}")
            
            # Update funding statistics
            funding_stats = overall_stats['funding']
            self.total_target_label.config(text=f"Total Target: ${funding_stats['total_target']:,.2f}")
            self.total_current_label.config(text=f"Total Current: ${funding_stats['total_current']:,.2f}")
            
            progress = funding_stats['overall_progress']
            self.overall_progress_label.config(text=f"Overall Progress: {progress:.1f}%")
            self.overall_progress_var.set(progress)
            
            # Load top projects
            self.load_top_projects()
            
        except Exception as e:
            print(f"Error loading statistics: {str(e)}")
    
    def load_top_projects(self):
        # Load top funded projects
        try:
            # Clear existing items
            for item in self.top_projects_tree.get_children():
                self.top_projects_tree.delete(item)
            
            # Get top projects
            top_projects = self.stats_controller.get_top_projects(10)
            
            # Add projects to treeview
            for i, project in enumerate(top_projects, 1):
                self.top_projects_tree.insert("", tk.END, values=(
                    i,
                    project['name'],
                    f"${project['current_amount']:,.2f}",
                    f"${project['target_amount']:,.2f}",
                    f"{project['progress_percentage']:.1f}%",
                    project['category']
                ))
                
        except Exception as e:
            print(f"Error loading top projects: {str(e)}")
    
    def show(self):
        # Show the statistics view
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.load_statistics()
    
    def hide(self):
        # Hide the statistics view
        self.frame.pack_forget()
