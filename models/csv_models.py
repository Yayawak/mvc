"""
CSV-based data models for CS Camp Crowdfunding System
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional
from enum import Enum

class PledgeStatus(Enum):
    SUCCESS = "SUCCESS"
    REJECTED = "REJECTED"

@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    created_at: datetime
    
    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at.replace(' ', 'T'))

@dataclass
class Category:
    id: int
    name: str
    description: str

@dataclass
class Project:
    id: str
    name: str
    description: str
    target_amount: float
    current_amount: float
    deadline: date
    category_id: int
    created_at: datetime
    
    def __post_init__(self):
        if isinstance(self.deadline, str):
            self.deadline = datetime.fromisoformat(self.deadline).date()
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at.replace(' ', 'T'))
    
    @property
    def progress_percentage(self):
        """Calculate funding progress percentage"""
        if self.target_amount == 0:
            return 0
        return min(100, (self.current_amount / self.target_amount) * 100)
    
    @property
    def is_active(self):
        """Check if project is still active (not past deadline)"""
        return self.deadline >= date.today()

@dataclass
class RewardTier:
    id: int
    project_id: str
    name: str
    description: str
    min_amount: float
    quota: int
    remaining_quota: int
    
    @property
    def is_available(self):
        """Check if reward tier has remaining quota"""
        return self.remaining_quota > 0

@dataclass
class Pledge:
    id: int
    user_id: int
    project_id: str
    reward_tier_id: Optional[int]
    amount: float
    status: PledgeStatus
    created_at: datetime
    
    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = PledgeStatus(self.status)
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at.replace(' ', 'T'))
        if self.reward_tier_id == '' or self.reward_tier_id is None:
            self.reward_tier_id = None
        else:
            self.reward_tier_id = int(self.reward_tier_id)
