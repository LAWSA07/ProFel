from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class JobSkill(BaseModel):
    """A skill required for a job."""
    name: str = Field(..., description="Name of the skill")
    importance: float = Field(0.5, description="Importance of the skill (0.0-1.0)", ge=0.0, le=1.0)

    class Config:
        schema_extra = {
            "example": {
                "name": "React",
                "importance": 0.8
            }
        }


class Job(BaseModel):
    """Job description with required skills."""
    id: Optional[str] = Field(None, description="Unique identifier for the job")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Optional[str] = Field("Remote", description="Job location")
    description: Optional[str] = Field(None, description="Job description text")
    skills: List[JobSkill] = Field(..., description="Required skills for the job")
    level: Optional[str] = Field(None, description="Job level (entry, mid, senior)")
    created_at: Optional[str] = Field(None, description="Timestamp when the job was created")

    class Config:
        schema_extra = {
            "example": {
                "id": "job123",
                "title": "Senior Frontend Developer",
                "company": "TechCorp Inc.",
                "location": "New York, NY",
                "description": "TechCorp is seeking an experienced Frontend Developer to lead UI development.",
                "skills": [
                    {"name": "React", "importance": 0.9},
                    {"name": "TypeScript", "importance": 0.8},
                    {"name": "CSS", "importance": 0.7},
                    {"name": "Redux", "importance": 0.6}
                ],
                "level": "senior",
                "created_at": "2023-11-15T10:30:00.000Z"
            }
        }


class JobRequest(BaseModel):
    """Request to create or process a job."""
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    skills_text: str = Field(..., description="Comma-separated list of required skills")
    location: Optional[str] = Field("Remote", description="Job location")

    class Config:
        schema_extra = {
            "example": {
                "title": "Senior Frontend Developer",
                "company": "TechCorp Inc.",
                "skills_text": "React, TypeScript, CSS, Redux, Jest, Webpack",
                "location": "New York, NY"
            }
        }