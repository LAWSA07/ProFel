from typing import List
from pydantic import BaseModel


class SkillMatch(BaseModel):
    """Represents a match between a job requirement and candidate skill"""
    skill: str
    job_importance: float  # How important is this skill for the job
    candidate_level: float  # How strong is the candidate in this skill
    match_score: float     # Combined score


class ProfileJobMatch(BaseModel):
    """
    Represents the match between a candidate profile and a job listing.
    """
    profile_name: str
    job_title: str
    company: str
    overall_match: float  # 0-100
    skill_matches: List[SkillMatch]
    missing_skills: List[str]
    strengths: List[str]
    recommendation: str