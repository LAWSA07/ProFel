from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class Skill(BaseModel):
    """A programming skill or technology."""
    name: str = Field(..., description="Name of the skill")
    proficiency: Optional[float] = Field(None, description="Proficiency level (0.0-1.0)", ge=0.0, le=1.0)

    class Config:
        schema_extra = {
            "example": {
                "name": "Python",
                "proficiency": 0.9
            }
        }


class Project(BaseModel):
    """A GitHub project or repository."""
    name: str = Field(..., description="Name of the project")
    description: Optional[str] = Field(None, description="Project description")
    technologies: List[str] = Field(default_factory=list, description="Technologies used in the project")
    url: Optional[HttpUrl] = Field(None, description="URL to the project repository")

    class Config:
        schema_extra = {
            "example": {
                "name": "personal-blog",
                "description": "A static blog built with Gatsby and React",
                "technologies": ["JavaScript", "React", "Gatsby", "GraphQL"],
                "url": "https://github.com/username/personal-blog"
            }
        }


class GitHubStats(BaseModel):
    """GitHub user statistics."""
    followers: Optional[int] = Field(0, description="Number of followers")
    following: Optional[int] = Field(0, description="Number of users following")
    contributions: Optional[int] = Field(0, description="Number of contributions")
    stars: Optional[int] = Field(0, description="Number of stars received")
    repositories: Optional[int] = Field(0, description="Number of repositories")

    class Config:
        schema_extra = {
            "example": {
                "followers": 120,
                "following": 45,
                "contributions": 850,
                "stars": 230,
                "repositories": 25
            }
        }


class GitHubProfile(BaseModel):
    """GitHub user profile data."""
    id: Optional[str] = Field(None, description="Unique identifier for the profile")
    username: str = Field(..., description="GitHub username")
    name: Optional[str] = Field(None, description="Full name of the user")
    bio: Optional[str] = Field(None, description="User biography")
    location: Optional[str] = Field(None, description="User location")
    skills: List[Skill] = Field(default_factory=list, description="List of skills")
    projects: List[Project] = Field(default_factory=list, description="List of projects")
    github_stats: Optional[GitHubStats] = Field(None, description="GitHub statistics")
    processed_at: Optional[str] = Field(None, description="Timestamp when the profile was processed")

    class Config:
        schema_extra = {
            "example": {
                "id": "abc123",
                "username": "johndoe",
                "name": "John Doe",
                "bio": "Full-stack developer specializing in React and Node.js",
                "location": "San Francisco, CA",
                "skills": [
                    {"name": "JavaScript", "proficiency": 0.9},
                    {"name": "React", "proficiency": 0.8},
                    {"name": "Node.js", "proficiency": 0.85}
                ],
                "projects": [
                    {
                        "name": "personal-blog",
                        "description": "A static blog built with Gatsby",
                        "technologies": ["JavaScript", "React", "Gatsby"],
                        "url": "https://github.com/johndoe/personal-blog"
                    }
                ],
                "github_stats": {
                    "followers": 120,
                    "following": 45,
                    "contributions": 850,
                    "stars": 230,
                    "repositories": 25
                },
                "processed_at": "2023-11-15T14:30:25.123Z"
            }
        }


class GitHubProfileRequest(BaseModel):
    """Request to process a GitHub profile."""
    username: str = Field(..., description="GitHub username to process")

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe"
            }
        }