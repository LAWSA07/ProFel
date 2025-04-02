from typing import List, Optional
from pydantic import BaseModel


class JobRequirement(BaseModel):
    """Represents a job requirement with its importance level"""
    skill: str
    importance: float  # 0-1 scale, where 1 is most important


class JobListing(BaseModel):
    """
    Represents the data structure of a job listing.
    """
    title: str
    company: str
    location: str
    description: str
    requirements: List[JobRequirement]
    salary_range: Optional[str] = None
    url: str