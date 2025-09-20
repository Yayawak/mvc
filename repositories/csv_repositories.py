"""
CSV-based repositories for data access
"""

import csv
import os
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from models.csv_models import User, Category, Project, RewardTier, Pledge, PledgeStatus

class CSVRepository:
    """Base class for CSV-based repositories"""
    
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.data_dir = "data"
        self.file_path = os.path.join(self.data_dir, csv_file)
    
    def _read_csv(self) -> List[Dict[str, Any]]:
        # Read data from CSV file
        if not os.path.exists(self.file_path):
            return []
        
        data = []
        with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    
    def _write_csv(self, data: List[Dict[str, Any]], fieldnames: List[str]):
        # Write data to CSV file
        os.makedirs(self.data_dir, exist_ok=True)
        
        with open(self.file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    def _get_next_id(self, data: List[Dict[str, Any]]) -> int:
        # Get next available ID
        if not data:
            return 1
        max_id = max(int(row.get('id', 0)) for row in data)
        return max_id + 1

class UserRepository(CSVRepository):
    def __init__(self):
        super().__init__("users.csv")
    
    def create(self, user: User) -> User:
        # Create a new user
        data = self._read_csv()
        user.id = self._get_next_id(data)
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'created_at': user.created_at.isoformat()
        }
        data.append(user_data)
        
        self._write_csv(data, ['id', 'username', 'email', 'password_hash', 'created_at'])
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        # Get user by ID
        data = self._read_csv()
        for row in data:
            if int(row['id']) == user_id:
                return User(
                    id=int(row['id']),
                    username=row['username'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=row['created_at']
                )
        return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        # Get user by username
        data = self._read_csv()
        for row in data:
            if row['username'] == username:
                return User(
                    id=int(row['id']),
                    username=row['username'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=row['created_at']
                )
        return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        # Get user by email
        data = self._read_csv()
        for row in data:
            if row['email'] == email:
                return User(
                    id=int(row['id']),
                    username=row['username'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=row['created_at']
                )
        return None
    
    def get_all(self) -> List[User]:
        # Get all users
        data = self._read_csv()
        users = []
        for row in data:
            users.append(User(
                id=int(row['id']),
                username=row['username'],
                email=row['email'],
                password_hash=row['password_hash'],
                created_at=row['created_at']
            ))
        return users
    
    def update(self, user: User) -> User:
        # Update user
        data = self._read_csv()
        for i, row in enumerate(data):
            if int(row['id']) == user.id:
                data[i] = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'password_hash': user.password_hash,
                    'created_at': user.created_at.isoformat()
                }
                break
        
        self._write_csv(data, ['id', 'username', 'email', 'password_hash', 'created_at'])
        return user

class CategoryRepository(CSVRepository):
    def __init__(self):
        super().__init__("categories.csv")
    
    def get_all(self) -> List[Category]:
        # Get all categories
        data = self._read_csv()
        categories = []
        for row in data:
            categories.append(Category(
                id=int(row['id']),
                name=row['name'],
                description=row['description']
            ))
        return categories
    
    def get_by_id(self, category_id: int) -> Optional[Category]:
        # Get category by ID
        data = self._read_csv()
        for row in data:
            if int(row['id']) == category_id:
                return Category(
                    id=int(row['id']),
                    name=row['name'],
                    description=row['description']
                )
        return None

class ProjectRepository(CSVRepository):
    def __init__(self):
        super().__init__("projects.csv")
    
    def get_all(self) -> List[Project]:
        # Get all projects
        data = self._read_csv()
        projects = []
        for row in data:
            projects.append(Project(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                target_amount=float(row['target_amount']),
                current_amount=float(row['current_amount']),
                deadline=row['deadline'],
                category_id=int(row['category_id']),
                created_at=row['created_at']
            ))
        return projects
    
    def get_by_id(self, project_id: str) -> Optional[Project]:
        # Get project by ID
        data = self._read_csv()
        for row in data:
            # Ensure both IDs are strings for comparison
            if str(row['id']) == str(project_id):
                return Project(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    target_amount=float(row['target_amount']),
                    current_amount=float(row['current_amount']),
                    deadline=row['deadline'],
                    category_id=int(row['category_id']),
                    created_at=row['created_at']
                )
        return None
    
    def get_by_category(self, category_id: int) -> List[Project]:
        # Get projects by category
        all_projects = self.get_all()
        return [p for p in all_projects if p.category_id == category_id]
    
    def search_by_name(self, search_term: str) -> List[Project]:
        # Search projects by name
        all_projects = self.get_all()
        return [p for p in all_projects if search_term.lower() in p.name.lower()]
    
    def get_sorted_by_newest(self) -> List[Project]:
        # Get projects sorted by newest first
        projects = self.get_all()
        return sorted(projects, key=lambda p: p.created_at, reverse=True)
    
    def get_sorted_by_deadline(self) -> List[Project]:
        # Get projects sorted by deadline (closest first)
        projects = self.get_all()
        return sorted(projects, key=lambda p: p.deadline)
    
    def get_sorted_by_funding(self) -> List[Project]:
        # Get projects sorted by funding amount (highest first)
        projects = self.get_all()
        return sorted(projects, key=lambda p: p.current_amount, reverse=True)
    
    def get_active_projects(self) -> List[Project]:
        # Get active projects (not past deadline)
        all_projects = self.get_all()
        return [p for p in all_projects if p.is_active]
    
    def update(self, project: Project) -> Project:
        # Update project
        data = self._read_csv()
        for i, row in enumerate(data):
            if row['id'] == str(project.id):
                data[i] = {
                    'id': project.id,
                    'name': project.name,
                    'description': project.description,
                    'target_amount': project.target_amount,
                    'current_amount': project.current_amount,
                    'deadline': project.deadline.isoformat(),
                    'category_id': project.category_id,
                    'created_at': project.created_at.isoformat()
                }
                break
        
        self._write_csv(data, ['id', 'name', 'description', 'target_amount', 'current_amount', 'deadline', 'category_id', 'created_at'])
        return project

class RewardRepository(CSVRepository):
    def __init__(self):
        super().__init__("reward_tiers.csv")
    
    def get_by_project(self, project_id: str) -> List[RewardTier]:
        # Get reward tiers by project ID
        data = self._read_csv()
        tiers = []
        for row in data:
            if row['project_id'] == str(project_id):
                tiers.append(RewardTier(
                    id=int(row['id']),
                    project_id=row['project_id'],
                    name=row['name'],
                    description=row['description'],
                    min_amount=float(row['min_amount']),
                    quota=int(row['quota']),
                    remaining_quota=int(row['remaining_quota'])
                ))
        return tiers
    
    def get_by_id(self, reward_id: int) -> Optional[RewardTier]:
        # Get reward tier by ID
        data = self._read_csv()
        for row in data:
            if int(row['id']) == reward_id:
                return RewardTier(
                    id=int(row['id']),
                    project_id=row['project_id'],
                    name=row['name'],
                    description=row['description'],
                    min_amount=float(row['min_amount']),
                    quota=int(row['quota']),
                    remaining_quota=int(row['remaining_quota'])
                )
        return None
    
    def get_available_by_project(self, project_id: str) -> List[RewardTier]:
        # Get available reward tiers by project ID
        all_tiers = self.get_by_project(project_id)
        return [t for t in all_tiers if t.is_available]
    
    def update(self, reward_tier: RewardTier) -> RewardTier:
        # Update reward tier
        data = self._read_csv()
        for i, row in enumerate(data):
            if int(row['id']) == reward_tier.id:
                data[i] = {
                    'id': reward_tier.id,
                    'project_id': reward_tier.project_id,
                    'name': reward_tier.name,
                    'description': reward_tier.description,
                    'min_amount': reward_tier.min_amount,
                    'quota': reward_tier.quota,
                    'remaining_quota': reward_tier.remaining_quota
                }
                break
        
        self._write_csv(data, ['id', 'project_id', 'name', 'description', 'min_amount', 'quota', 'remaining_quota'])
        return reward_tier
    
    def decrease_quota(self, reward_id: int) -> bool:
        # Decrease remaining quota by 1
        data = self._read_csv()
        for i, row in enumerate(data):
            if int(row['id']) == reward_id:
                current_quota = int(row['remaining_quota'])
                if current_quota > 0:
                    data[i]['remaining_quota'] = str(current_quota - 1)
                    self._write_csv(data, ['id', 'project_id', 'name', 'description', 'min_amount', 'quota', 'remaining_quota'])
                    return True
        return False

class PledgeRepository(CSVRepository):
    def __init__(self):
        super().__init__("pledges.csv")
    
    def create(self, pledge: Pledge) -> Pledge:
        # Create a new pledge
        data = self._read_csv()
        pledge.id = self._get_next_id(data)
        
        pledge_data = {
            'id': pledge.id,
            'user_id': pledge.user_id,
            'project_id': pledge.project_id,
            'reward_tier_id': pledge.reward_tier_id or '',
            'amount': pledge.amount,
            'status': pledge.status.value,
            'created_at': pledge.created_at.isoformat()
        }
        data.append(pledge_data)
        
        self._write_csv(data, ['id', 'user_id', 'project_id', 'reward_tier_id', 'amount', 'status', 'created_at'])
        return pledge
    
    def get_by_user(self, user_id: int) -> List[Pledge]:
        # Get pledges by user ID
        data = self._read_csv()
        pledges = []
        for row in data:
            if int(row['user_id']) == user_id:
                pledges.append(Pledge(
                    id=int(row['id']),
                    user_id=int(row['user_id']),
                    project_id=row['project_id'],
                    reward_tier_id=int(row['reward_tier_id']) if row['reward_tier_id'] else None,
                    amount=float(row['amount']),
                    status=row['status'],
                    created_at=row['created_at']
                ))
        return pledges
    
    def get_by_project(self, project_id: str) -> List[Pledge]:
        # Get pledges by project ID
        data = self._read_csv()
        pledges = []
        for row in data:
            if row['project_id'] == str(project_id):
                pledges.append(Pledge(
                    id=int(row['id']),
                    user_id=int(row['user_id']),
                    project_id=row['project_id'],
                    reward_tier_id=int(row['reward_tier_id']) if row['reward_tier_id'] else None,
                    amount=float(row['amount']),
                    status=row['status'],
                    created_at=row['created_at']
                ))
        return pledges
    
    def get_by_status(self, status: PledgeStatus) -> List[Pledge]:
        # Get pledges by status
        data = self._read_csv()
        pledges = []
        for row in data:
            if row['status'] == status.value:
                pledges.append(Pledge(
                    id=int(row['id']),
                    user_id=int(row['user_id']),
                    project_id=row['project_id'],
                    reward_tier_id=int(row['reward_tier_id']) if row['reward_tier_id'] else None,
                    amount=float(row['amount']),
                    status=row['status'],
                    created_at=row['created_at']
                ))
        return pledges
    
    def get_successful_by_project(self, project_id: str) -> List[Pledge]:
        # Get successful pledges by project ID
        all_pledges = self.get_by_project(project_id)
        return [p for p in all_pledges if p.status == PledgeStatus.SUCCESS]
    
    def get_rejected_by_project(self, project_id: str) -> List[Pledge]:
        # Get rejected pledges by project ID
        all_pledges = self.get_by_project(project_id)
        return [p for p in all_pledges if p.status == PledgeStatus.REJECTED]
    
    def get_statistics(self) -> Dict[str, int]:
        # Get pledge statistics
        data = self._read_csv()
        total = len(data)
        successful = len([row for row in data if row['status'] == 'SUCCESS'])
        rejected = len([row for row in data if row['status'] == 'REJECTED'])
        
        return {
            'total': total,
            'successful': successful,
            'rejected': rejected
        }
    
    def get_project_statistics(self, project_id: str) -> Dict[str, int]:
        # Get pledge statistics for a specific project
        project_pledges = self.get_by_project(project_id)
        total = len(project_pledges)
        successful = len([p for p in project_pledges if p.status == PledgeStatus.SUCCESS])
        rejected = len([p for p in project_pledges if p.status == PledgeStatus.REJECTED])
        
        return {
            'total': total,
            'successful': successful,
            'rejected': rejected
        }
