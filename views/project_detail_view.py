import tkinter as tk
from tkinter import ttk, messagebox
from controllers.csv_controllers import ProjectsController
from models.csv_models import Project
from typing import Dict, Any, Callable, Optional

class ProjectDetailView:
    def __init__(self, parent, projects_controller: ProjectsController,
                 on_back: Callable):
        self.parent = parent
        self.projects_controller = projects_controller
        self.on_back = on_back
        
        self.frame = ttk.Frame(parent)
        self.current_project_id: Optional[str] = None
        self.tier_data = {}  # Initialize tier data storage
        self.setup_ui()
    
    def setup_ui(self):
        # Setup the project detail UI
        # Header frame
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Back button
        back_btn = ttk.Button(header_frame, text="← Back to Projects", command=self.on_back)
        back_btn.pack(side=tk.LEFT)
        
        # Title (will be set when project is loaded)
        self.title_label = ttk.Label(header_frame, text="", font=("Arial", 16, "bold"))
        self.title_label.pack(side=tk.RIGHT)
        
        # Main content frame
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Project info
        left_frame = ttk.LabelFrame(main_frame, text="Project Information", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Project details
        self.project_id_label = ttk.Label(left_frame, text="")
        self.project_id_label.pack(anchor=tk.W, pady=2)
        
        self.description_label = ttk.Label(left_frame, text="", wraplength=400)
        self.description_label.pack(anchor=tk.W, pady=2)
        
        self.target_label = ttk.Label(left_frame, text="")
        self.target_label.pack(anchor=tk.W, pady=2)
        
        self.current_label = ttk.Label(left_frame, text="")
        self.current_label.pack(anchor=tk.W, pady=2)
        
        # Progress bar
        ttk.Label(left_frame, text="Progress:").pack(anchor=tk.W, pady=(10, 2))
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(left_frame, variable=self.progress_var, 
                                          maximum=100, length=300)
        self.progress_bar.pack(anchor=tk.W, pady=2)
        
        self.progress_label = ttk.Label(left_frame, text="")
        self.progress_label.pack(anchor=tk.W, pady=2)
        
        self.deadline_label = ttk.Label(left_frame, text="")
        self.deadline_label.pack(anchor=tk.W, pady=2)
        
        self.status_label = ttk.Label(left_frame, text="", font=("Arial", 10, "bold"))
        self.status_label.pack(anchor=tk.W, pady=5)
        
        # Right panel - Pledge form
        right_frame = ttk.LabelFrame(main_frame, text="Make a Pledge", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # Pledge amount
        ttk.Label(right_frame, text="Pledge Amount ($):").pack(anchor=tk.W, pady=2)
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(right_frame, textvariable=self.amount_var, width=20)
        amount_entry.pack(anchor=tk.W, pady=2)
        
        # Reward tier selection
        ttk.Label(right_frame, text="Reward Tier (Optional):").pack(anchor=tk.W, pady=(10, 2))
        self.reward_var = tk.StringVar()
        self.reward_combo = ttk.Combobox(right_frame, textvariable=self.reward_var, 
                                        state="readonly", width=20)
        self.reward_combo.pack(anchor=tk.W, pady=2)
        
        # Initialize with default values
        self.reward_combo['values'] = ["No reward tier"]
        self.reward_combo.set("No reward tier")
        
        # Pledge button
        pledge_btn = ttk.Button(right_frame, text="Make Pledge", command=self.make_pledge)
        pledge_btn.pack(pady=10)
        
        # Reward tiers list
        tiers_frame = ttk.LabelFrame(right_frame, text="Available Reward Tiers", padding=5)
        tiers_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview for reward tiers
        self.tiers_tree = ttk.Treeview(tiers_frame, columns=("Name", "Min Amount", "Quota"), 
                                      show="headings", height=8)
        self.tiers_tree.heading("Name", text="Name")
        self.tiers_tree.heading("Min Amount", text="Min Amount")
        self.tiers_tree.heading("Quota", text="Remaining")
        
        self.tiers_tree.column("Name", width=150)
        self.tiers_tree.column("Min Amount", width=80)
        self.tiers_tree.column("Quota", width=60)
        
        tiers_scrollbar = ttk.Scrollbar(tiers_frame, orient=tk.VERTICAL, 
                                      command=self.tiers_tree.yview)
        self.tiers_tree.configure(yscrollcommand=tiers_scrollbar.set)
        
        self.tiers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tiers_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.tiers_tree.bind('<<TreeviewSelect>>', self.on_tier_select)
    
    def load_project(self, project_id: str):
        # Load project details
        try:
            self.current_project_id = project_id
            
            # Validate controller
            if not self.projects_controller:
                messagebox.showerror("Error", "Controller not initialized")
                return
            
            # Get project data from controller
            project_data = self.projects_controller.get_project_details(project_id)
            
            # Check if we got valid data
            if not project_data or not isinstance(project_data, dict):
                messagebox.showerror("Error", "Project not found")
                return
            
            # Check if required keys exist
            if 'project' not in project_data:
                messagebox.showerror("Error", "Invalid project data")
                return
            
            project = project_data['project']
            reward_tiers = project_data.get('reward_tiers', [])
            stats = project_data.get('statistics', {})
            
            # Update project info
            self.title_label.config(text=project.name)
            self.project_id_label.config(text=f"Project ID: {project.id}")
            self.description_label.config(text=f"Description: {project.description or 'No description'}")
            self.target_label.config(text=f"Target Amount: ${project.target_amount:,.2f}")
            self.current_label.config(text=f"Current Amount: ${project.current_amount:,.2f}")
            self.deadline_label.config(text=f"Deadline: {project.deadline.strftime('%Y-%m-%d')}")
            
            # Progress bar
            progress = project.progress_percentage
            self.progress_var.set(progress)
            self.progress_label.config(text=f"{progress:.1f}% funded")
            
            # Status
            if project.is_active:
                self.status_label.config(text="Status: Active", foreground="green")
            else:
                self.status_label.config(text="Status: Expired", foreground="red")
            
            # Load reward tiers
            self.load_reward_tiers(reward_tiers)
            
        except Exception as e:
            error_msg = f"Failed to load project: {str(e)}"
            print(f"Exception in load_project: {error_msg}")
            messagebox.showerror("Error", error_msg)
    
    def load_reward_tiers(self, reward_tiers):
        # Load reward tiers into the treeview
        # Clear existing items
        for item in self.tiers_tree.get_children():
            self.tiers_tree.delete(item)
        
        # Update combobox
        tier_options = ["No reward tier"]
        self.tier_data = {}  # Store as instance variable

        
        for tier in reward_tiers:
            if tier['is_available']:
                tier_options.append(f"{tier['name']} (${tier['min_amount']:.2f})")
                self.tier_data[f"{tier['name']} (${tier['min_amount']:.2f})"] = tier
        
        # Update combobox with new values
        self.reward_combo['values'] = tier_options
        self.reward_combo.set("No reward tier")
        
        # Force UI refresh
        self.reward_combo.update_idletasks()
        self.tiers_tree.update_idletasks()
        
        # Add to treeview
        for tier in reward_tiers:
            self.tiers_tree.insert("", tk.END, values=(
                tier['name'],
                f"${tier['min_amount']:.2f}",
                f"{tier['remaining_quota']}/{tier['quota']}"
            ))
    
    def on_tier_select(self, event):
        # Handle reward tier selection
        selection = self.tiers_tree.selection()
        if selection:
            item = self.tiers_tree.item(selection[0])
            tier_name = item['values'][0]
            min_amount = item['values'][1].replace('$', '').replace(',', '')
            
            # Update combobox selection
            self.reward_combo.set(f"{tier_name} (${min_amount})")
            
            # Set minimum amount
            self.amount_var.set(min_amount)
    
    def make_pledge(self):
        # Handle pledge submission
        if not self.current_project_id:
            messagebox.showerror("Error", "No project selected")
            return
        
        try:
            amount = float(self.amount_var.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            return
        
        # Get selected reward tier
        reward_tier_id = None
        selected_tier = self.reward_combo.get()
        if selected_tier != "No reward tier":
            # Find the corresponding reward tier
            project_data = self.projects_controller.get_project_details(self.current_project_id)
            for tier in project_data['reward_tiers']:
                if f"{tier['name']} (${tier['min_amount']:.2f})" == selected_tier:
                    reward_tier_id = tier['id']
                    break
        
        # Make the pledge (using a default user ID since no auth)
        # In a real system, you might want to ask for user info
        default_user_id = 1  # Use first user as default
        success, message = self.projects_controller.create_pledge(
            default_user_id, self.current_project_id, amount, reward_tier_id
        )
        
        if success:
            messagebox.showinfo("Success", message)
            # Reload project to show updated amounts
            self.load_project(self.current_project_id)
        else:
            messagebox.showerror("Pledge Failed", message)
    
    def show(self):
        # Show the project detail view
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        # Hide the project detail view
        self.frame.pack_forget()
