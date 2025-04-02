from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SkillMatch(BaseModel):
    """Match result for a single skill."""
    skill_name: str = Field(..., description="Name of the skill")
    importance: float = Field(..., description="Importance of the skill (0.0-1.0)")
    match_score: float = Field(..., description="Match score for this skill (0.0-1.0)")
    weighted_score: float = Field(..., description="Weighted score (importance * match_score)")

    class Config:
        schema_extra = {
            "example": {
                "skill_name": "React",
                "importance": 0.9,
                "match_score": 0.8,
                "weighted_score": 0.72
            }
        }


class MatchResult(BaseModel):
    """Result of matching a profile to a job."""
    profile_name: str = Field(..., description="Name of the profile")
    job_title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    overall_match: float = Field(..., description="Overall match percentage (0-100)")
    skill_matches: List[SkillMatch] = Field(default_factory=list, description="Detailed skill matches")
    missing_skills: List[str] = Field(default_factory=list, description="Skills missing from the profile")
    strengths: List[str] = Field(default_factory=list, description="Strengths (high-matching important skills)")
    recommendation: str = Field(..., description="Match recommendation")

    class Config:
        schema_extra = {
            "example": {
                "profile_name": "John Doe",
                "job_title": "Senior Frontend Developer",
                "company": "TechCorp Inc.",
                "overall_match": 75,
                "skill_matches": [
                    {
                        "skill_name": "React",
                        "importance": 0.9,
                        "match_score": 1.0,
                        "weighted_score": 0.9
                    },
                    {
                        "skill_name": "TypeScript",
                        "importance": 0.8,
                        "match_score": 0.7,
                        "weighted_score": 0.56
                    }
                ],
                "missing_skills": ["Redux", "Jest"],
                "strengths": ["React"],
                "recommendation": "Good Match: This candidate has many of the required skills and would likely be a good fit with some training."
            }
        }


class ProfileJobMatchRequest(BaseModel):
    """Request to match a profile to a job."""
    profile: Dict[str, Any] = Field(..., description="Profile data")
    job: Dict[str, Any] = Field(..., description="Job data")

    class Config:
        schema_extra = {
            "example": {
                "profile": {
                    "name": "John Doe",
                    "skills": [
                        {"name": "JavaScript"},
                        {"name": "React"},
                        {"name": "HTML/CSS"}
                    ]
                },
                "job": {
                    "title": "Frontend Developer",
                    "company": "TechCorp",
                    "skills": [
                        {"name": "JavaScript", "importance": 0.9},
                        {"name": "React", "importance": 0.8},
                        {"name": "TypeScript", "importance": 0.7}
                    ]
                }
            }
        }


class BatchMatchRequest(BaseModel):
    """Request to match multiple profiles against multiple jobs."""
    profiles: List[Dict[str, Any]] = Field(..., description="List of profiles")
    jobs: List[Dict[str, Any]] = Field(..., description="List of jobs")

    class Config:
        schema_extra = {
            "example": {
                "profiles": [
                    {
                        "name": "John Doe",
                        "skills": [
                            {"name": "JavaScript"},
                            {"name": "React"},
                            {"name": "HTML/CSS"}
                        ]
                    },
                    {
                        "name": "Jane Smith",
                        "skills": [
                            {"name": "Python"},
                            {"name": "Django"},
                            {"name": "SQL"}
                        ]
                    }
                ],
                "jobs": [
                    {
                        "title": "Frontend Developer",
                        "company": "TechCorp",
                        "skills": [
                            {"name": "JavaScript", "importance": 0.9},
                            {"name": "React", "importance": 0.8},
                            {"name": "TypeScript", "importance": 0.7}
                        ]
                    },
                    {
                        "title": "Backend Developer",
                        "company": "DataSystems",
                        "skills": [
                            {"name": "Python", "importance": 0.9},
                            {"name": "Django", "importance": 0.8},
                            {"name": "SQL", "importance": 0.7},
                            {"name": "Docker", "importance": 0.6}
                        ]
                    }
                ]
            }
        }