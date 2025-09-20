"""
CSV-based services for business logic
"""

from typing import Optional, List, Dict, Any, Tuple
from datetime import date, datetime
import hashlib

from repositories.csv_repositories import (
    UserRepository, CategoryRepository, ProjectRepository, 
    RewardRepository, PledgeRepository
)
from models.csv_models import User, Project, RewardTier, Pledge, PledgeStatus

class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        self.current_user: Optional[User] = None
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        return self.hash_password(password) == hashed
    
    def register(self, username: str, email: str, password: str) -> Optional[User]:
        if self.user_repo.get_by_username(username):
            raise ValueError("Username already exists")
        
        if self.user_repo.get_by_email(email):
            raise ValueError("Email already exists")
        
        # Create new user
        hashed_password = self.hash_password(password)
        user = User(
            id=0, 
            username=username,
            email=email,
            password_hash=hashed_password,
            created_at=datetime.now()
        )
        
        return self.user_repo.create(user)
    
    def login(self, username: str, password: str) -> bool:
        user = self.user_repo.get_by_username(username)
        if user and self.verify_password(password, user.password_hash):
            self.current_user = user
            return True
        return False
    
    def logout(self):
        self.current_user = None
    
    def get_current_user(self) -> Optional[User]:
        return self.current_user
    
    def is_logged_in(self) -> bool:
        return self.current_user is not None

class ProjectService:
    def __init__(self, project_repo, category_repo, reward_repo):
        self.project_repo = project_repo
        self.reward_repo = reward_repo
        self.category_repo = category_repo
    
    def get_all_projects(self) -> List[Project]:
        return self.project_repo.get_all()
    
    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        return self.project_repo.get_by_id(project_id)
    
    def search_projects(self, search_term: str) -> List[Project]:
        return self.project_repo.search_by_name(search_term)
    
    def get_projects_by_category(self, category_id: int) -> List[Project]:
        return self.project_repo.get_by_category(category_id)
    
    def get_projects_sorted(self, sort_by: str) -> List[Project]:
        if sort_by == "newest":
            return self.project_repo.get_sorted_by_newest()
        elif sort_by == "deadline":
            return self.project_repo.get_sorted_by_deadline()
        elif sort_by == "funding":
            return self.project_repo.get_sorted_by_funding()
        else:
            return self.project_repo.get_all()
    
    def get_active_projects(self) -> List[Project]:
        return self.project_repo.get_active_projects()
    
    def get_project_details(self, project_id: str) -> Optional[Dict[str, Any]]:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            return None
        
        # print("reward_repo")
        # print(self.reward_repo)
        # print(project)
        # Get reward tiers
        reward_tiers = self.reward_repo.get_by_project(project_id)
        # print("reward_tiers", reward_tiers)
        
        # Format reward tiers for the view
        formatted_tiers = []
        for tier in reward_tiers:
            formatted_tiers.append({
                'id': tier.id,
                'name': tier.name,
                'description': tier.description,
                'min_amount': tier.min_amount,
                'quota': tier.quota,
                'remaining_quota': tier.remaining_quota,
                'is_available': tier.is_available
            })
        
        # Get pledge statistics
        pledge_repo = PledgeRepository()
        stats = pledge_repo.get_project_statistics(project_id)
        
        return {
            'project': project,
            'reward_tiers': formatted_tiers,
            'statistics': stats,
            'progress_percentage': project.progress_percentage,
            'is_active': project.is_active
        }
    
    def update_project_amount(self, project_id: str, amount: float):
        project = self.project_repo.get_by_id(project_id)
        if project:
            project.current_amount += amount
            self.project_repo.update(project)
    
    def get_category_name(self, category_id: int) -> str:
        category = self.category_repo.get_by_id(category_id)
        return category.name if category else "Unknown"

class PledgeService:
    def __init__(self, pledge_repo, project_repo, reward_repo):
        self.pledge_repo = pledge_repo
        self.project_repo = project_repo
        self.reward_repo = reward_repo
        # Create a ProjectService instance with the same repositories
        self.project_service = ProjectService(project_repo, None, reward_repo)
    
    def create_pledge(self, user_id: int, project_id: str, amount: float, 
                     reward_tier_id: Optional[int] = None) -> Pledge:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found c")
        
        if not project.is_active:
            raise ValueError("Project deadline has passed")
        
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
        if reward_tier_id:
            reward_tier = self.reward_repo.get_by_id(reward_tier_id)
            if not reward_tier:
                raise ValueError("Reward tier not found")
            
            if int(reward_tier.project_id) != int(project_id):
                raise ValueError("Reward tier does not belong to this project a")
            
            if not reward_tier.is_available:
                raise ValueError("Reward tier quota is full")
            
            if amount < reward_tier.min_amount:
                raise ValueError(f"Amount must be at least {reward_tier.min_amount} for this reward tier")
        
        # Create pledge
        pledge = Pledge(
            id=0,  # Will be set by repository
            user_id=user_id,
            project_id=project_id,
            reward_tier_id=reward_tier_id,
            amount=amount,
            status=PledgeStatus.SUCCESS,
            created_at=datetime.now()
        )
        
        # Save pledge
        created_pledge = self.pledge_repo.create(pledge)
        
        # Update project amount
        self.project_service.update_project_amount(project_id, amount)
        
        # Decrease reward tier quota if applicable
        if reward_tier_id:
            self.reward_repo.decrease_quota(reward_tier_id)
        
        return created_pledge
    
    def create_rejected_pledge(self, user_id: int, project_id: str, amount: float, 
                              reward_tier_id: Optional[int] = None, reason: str = "") -> Pledge:
        # Create a rejected pledge for tracking purposes
        pledge = Pledge(
            id=0,  # Will be set by repository
            user_id=user_id,
            project_id=project_id,
            reward_tier_id=reward_tier_id,
            amount=amount,
            status=PledgeStatus.REJECTED,
            created_at=datetime.now()
        )
        
        return self.pledge_repo.create(pledge)
    
    def get_pledges_by_user(self, user_id: int) -> List[Pledge]:
        return self.pledge_repo.get_by_user(user_id)
    
    def get_pledges_by_project(self, project_id: str) -> List[Pledge]:
        return self.pledge_repo.get_by_project(project_id)
    
    def get_successful_pledges_by_project(self, project_id: str) -> List[Pledge]:
        return self.pledge_repo.get_successful_by_project(project_id)
    
    def get_rejected_pledges_by_project(self, project_id: str) -> List[Pledge]:
        return self.pledge_repo.get_rejected_by_project(project_id)
    
    def get_statistics(self) -> Dict[str, int]:
        return self.pledge_repo.get_statistics()
    
    def get_project_statistics(self, project_id: str) -> Dict[str, int]:
        return self.pledge_repo.get_project_statistics(project_id)
    
    def validate_pledge(self, user_id: int, project_id: str, amount: float, 
                       reward_tier_id: Optional[int] = None) -> Tuple[bool, str]:
        try:
            # Check project exists and is active
            project = self.project_repo.get_by_id(project_id)
            if not project:
                return False, "Project not found b"
            
            if not project.is_active:
                return False, "Project deadline has passed"
            
            # Check amount
            if amount <= 0:
                return False, "Amount must be greater than 0"
            
            # Check reward tier if provided
            if reward_tier_id:
                reward_tier = self.reward_repo.get_by_id(reward_tier_id)
                if not reward_tier:
                    return False, "Reward tier not found"
                
                if int(reward_tier.project_id) != int(project_id):
                    return False, "Reward tier does not belong to this project b"
                
                if not reward_tier.is_available:
                    return False, "Reward tier quota is full"
                
                if amount < reward_tier.min_amount:
                    return False, f"Amount must be at least {reward_tier.min_amount} for this reward tier"
            
            return True, "Valid pledge"
            
        except Exception as e:
            return False, str(e)
