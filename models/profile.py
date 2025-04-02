from typing import List, Optional, Dict
from pydantic import BaseModel


class Skill(BaseModel):
    """Represents a professional skill"""
    name: str
    level: Optional[str] = None

class Project(BaseModel):
    """Represents a project in a profile"""
    name: str
    description: str
    technologies: List[str]
    url: Optional[str] = None

class Certification(BaseModel):
    """Represents a professional certification"""
    name: str
    issuer: str
    date: Optional[str] = None
    url: Optional[str] = None

class Connection(BaseModel):
    """Represents a professional connection"""
    name: str
    company: Optional[str] = None
    position: Optional[str] = None

class Profile(BaseModel):
    """
    Represents the data structure of a user profile with information from multiple sources.
    """
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    skills: List[Skill]
    projects: List[Project] = []
    certifications: List[Certification] = []
    connections: List[Connection] = []
    github_stats: Optional[Dict] = None
    leetcode_stats: Optional[Dict] = None
    linkedin_details: Optional[Dict] = None