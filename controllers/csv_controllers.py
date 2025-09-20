"""
CSV-based controllers for view coordination
"""

from typing import Optional, Callable, Dict, Any, List
from services.csv_services import AuthService, ProjectService, PledgeService
from repositories.csv_repositories import (
    UserRepository, CategoryRepository, ProjectRepository,
    RewardRepository, PledgeRepository
)
from models.csv_models import User, Project, Pledge

class AuthController:
    def __init__(self):
        # Initialize repositories
        user_repo = UserRepository()
        
        # Initialize service with repository
        self.auth_service = AuthService(user_repo)
        self.on_login_callback: Optional[Callable] = None
        self.on_logout_callback: Optional[Callable] = None
    
    def set_login_callback(self, callback: Callable):
        # Set callback to be called on successful login
        self.on_login_callback = callback
    
    def set_logout_callback(self, callback: Callable):
        # Set callback to be called on logout
        self.on_logout_callback = callback
    
    def login(self, username: str, password: str) -> tuple[bool, str]:
        # Handle login request
        try:
            success = self.auth_service.login(username, password)
            if success:
                if self.on_login_callback:
                    self.on_login_callback()
                return True, "Login successful"
            else:
                return False, "Invalid username or password"
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    def logout(self) -> bool:
        # Handle logout request
        try:
            self.auth_service.logout()
            if self.on_logout_callback:
                self.on_logout_callback()
            return True
        except Exception as e:
            return False
    
    def register(self, username: str, email: str, password: str) -> tuple[bool, str]:
        # Handle registration request
        try:
            user = self.auth_service.register(username, email, password)
            return True, f"Registration successful for user: {user.username}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    def get_current_user(self) -> Optional[User]:
        # Get current logged in user
        return self.auth_service.get_current_user()
    
    def is_logged_in(self) -> bool:
        # Check if user is logged in
        return self.auth_service.is_logged_in()

class ProjectsController:
    def __init__(self):
        # Initialize repositories
        project_repo = ProjectRepository()
        category_repo = CategoryRepository()
        reward_tier_repo = RewardRepository()
        pledge_repo = PledgeRepository()
        
        # Initialize services with repositories
        self.project_service = ProjectService(project_repo, category_repo, reward_tier_repo)
        self.pledge_service = PledgeService(pledge_repo, project_repo, reward_tier_repo)
    
    def get_all_projects(self) -> List[Project]:
        # Get all projects
        return self.project_service.get_all_projects()
    
    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        # Get project by ID
        return self.project_service.get_project_by_id(project_id)
    
    def search_projects(self, search_term: str) -> List[Project]:
        # Search projects by name
        return self.project_service.search_projects(search_term)
    
    def get_projects_by_category(self, category_id: int) -> List[Project]:
        # Get projects by category
        return self.project_service.get_projects_by_category(category_id)
    
    def get_projects_sorted(self, sort_by: str) -> List[Project]:
        # Get projects sorted by criteria
        return self.project_service.get_projects_sorted(sort_by)
    
    def get_active_projects(self) -> List[Project]:
        # Get active projects
        return self.project_service.get_active_projects()
    
    def get_project_details(self, project_id: str) -> Optional[Dict[str, Any]]:
        # Get detailed project information
        return self.project_service.get_project_details(project_id)
    
    def create_pledge(self, user_id: int, project_id: str, amount: float, 
                     reward_tier_id: Optional[int] = None) -> tuple[bool, str]:
        # Create a pledge for a project
        try:
            # Validate pledge first
            is_valid, message = self.pledge_service.validate_pledge(
                user_id, project_id, amount, reward_tier_id
            )
            
            if not is_valid:
                # Create rejected pledge for tracking
                self.pledge_service.create_rejected_pledge(
                    user_id, project_id, amount, reward_tier_id, message
                )
                return False, message
            
            # Create successful pledge
            pledge = self.pledge_service.create_pledge(
                user_id, project_id, amount, reward_tier_id
            )
            return True, f"Pledge successful! Amount: ${amount}"
            
        except Exception as e:
            # Create rejected pledge for tracking
            self.pledge_service.create_rejected_pledge(
                user_id, project_id, amount, reward_tier_id, str(e)
            )
            return False, f"Pledge failed: {str(e)}"
    
    def get_project_statistics(self, project_id: str) -> Dict[str, int]:
        # Get project pledge statistics
        return self.pledge_service.get_project_statistics(project_id)
    
    def get_category_name(self, category_id: int) -> str:
        # Get category name by ID
        return self.project_service.get_category_name(category_id)

class StatsController:
    def __init__(self):
        # Initialize repositories
        project_repo = ProjectRepository()
        category_repo = CategoryRepository()
        reward_tier_repo = RewardRepository()
        pledge_repo = PledgeRepository()
        
        # Initialize services with repositories
        self.pledge_service = PledgeService(pledge_repo, project_repo, reward_tier_repo)
        self.project_service = ProjectService(project_repo, category_repo, reward_tier_repo)
    
    def get_overall_statistics(self) -> Dict[str, Any]:
        # Get overall system statistics
        pledge_stats = self.pledge_service.get_statistics()
        
        # Get project statistics
        all_projects = self.project_service.get_all_projects()
        active_projects = self.project_service.get_active_projects()
        
        total_target = sum(p.target_amount for p in all_projects)
        total_current = sum(p.current_amount for p in all_projects)
        
        return {
            'pledges': pledge_stats,
            'projects': {
                'total': len(all_projects),
                'active': len(active_projects),
                'completed': len(all_projects) - len(active_projects)
            },
            'funding': {
                'total_target': total_target,
                'total_current': total_current,
                'overall_progress': (total_current / total_target * 100) if total_target > 0 else 0
            }
        }
    
    def get_project_statistics(self, project_id: str) -> Dict[str, Any]:
        # Get statistics for a specific project
        project = self.project_service.get_project_by_id(project_id)
        if not project:
            return {}
        
        pledge_stats = self.pledge_service.get_project_statistics(project_id)
        
        return {
            'project': {
                'name': project.name,
                'target_amount': project.target_amount,
                'current_amount': project.current_amount,
                'progress_percentage': project.progress_percentage,
                'deadline': project.deadline,
                'is_active': project.is_active
            },
            'pledges': pledge_stats
        }
    
    def get_successful_pledges(self) -> List[Dict[str, Any]]:
        # Get list of successful pledges
        # This would need to be implemented in the service layer
        # For now, return empty list
        return []
    
    def get_rejected_pledges(self) -> List[Dict[str, Any]]:
        # Get list of rejected pledges
        # This would need to be implemented in the service layer
        # For now, return empty list
        return []
    
    def get_top_projects(self, limit: int = 5) -> List[Dict[str, Any]]:
        # Get top funded projects
        projects = self.project_service.get_projects_sorted('funding')
        top_projects = []
        
        for project in projects[:limit]:
            # Get category name
            from repositories.csv_repositories import CategoryRepository
            category_repo = CategoryRepository()
            category = category_repo.get_by_id(project.category_id)
            category_name = category.name if category else 'Unknown'
            
            top_projects.append({
                'id': project.id,
                'name': project.name,
                'current_amount': project.current_amount,
                'target_amount': project.target_amount,
                'progress_percentage': project.progress_percentage,
                'category': category_name
            })
        
        return top_projects
