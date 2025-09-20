import tkinter as tk
from tkinter import ttk, messagebox
from controllers.csv_controllers import AuthController
from typing import Callable, Optional

class LoginView:
    def __init__(self, parent, auth_controller: AuthController, on_login_success: Callable):
        self.parent = parent
        self.auth_controller = auth_controller
        self.on_login_success = on_login_success
        
        self.frame = ttk.Frame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Setup the login UI
        # Main container
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        # Title
        title_label = ttk.Label(main_frame, text="CS Camp Crowdfunding System", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 30))
        
        # Login form
        login_frame = ttk.LabelFrame(main_frame, text="Login", padding=20)
        login_frame.pack(fill=tk.X, pady=10)
        
        # Username
        ttk.Label(login_frame, text="Username:").pack(anchor=tk.W, pady=(0, 5))
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(login_frame, textvariable=self.username_var, width=30)
        username_entry.pack(anchor=tk.W, pady=(0, 15))
        
        # Password
        ttk.Label(login_frame, text="Password:").pack(anchor=tk.W, pady=(0, 5))
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(login_frame, textvariable=self.password_var, 
                                  show="*", width=30)
        password_entry.pack(anchor=tk.W, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        login_btn = ttk.Button(button_frame, text="Login", command=self.login)
        login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        register_btn = ttk.Button(button_frame, text="Register", command=self.register)
        register_btn.pack(side=tk.LEFT)
        
        # Sample users info
        info_frame = ttk.LabelFrame(main_frame, text="Sample Users (for testing)", padding=10)
        info_frame.pack(fill=tk.X, pady=20)
        
        sample_users = [
            "john_doe", "jane_smith", "mike_wilson", "sarah_jones", "alex_brown",
            "emma_davis", "david_lee", "lisa_wang", "tom_chen", "anna_kim"
        ]
        
        ttk.Label(info_frame, text="Available usernames (password: 'password'):").pack(anchor=tk.W)
        ttk.Label(info_frame, text=", ".join(sample_users), 
                 font=("Arial", 9)).pack(anchor=tk.W, pady=5)
        
        # Bind Enter key to login
        username_entry.bind('<Return>', lambda e: self.login())
        password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        # Handle login
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        success, message = self.auth_controller.login(username, password)
        
        if success:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.on_login_success()
        else:
            messagebox.showerror("Error", message)
    
    def register(self):
        # Mock registration - just show a message
        messagebox.showinfo("Registration", "Registration feature is not implemented.\nPlease use one of the existing sample users:\n\njohn_doe, jane_smith, mike_wilson, sarah_jones, alex_brown,\nemma_davis, david_lee, lisa_wang, tom_chen, anna_kim\n\nPassword: 'password'")
    
    def show(self):
        # Show the login view
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        # Hide the login view
        self.frame.pack_forget()
