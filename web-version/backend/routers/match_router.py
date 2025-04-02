from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

from services.match_service import match_profile_to_job

router = APIRouter()

class Profile(BaseModel):
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    skills: List[Dict]
    projects: List[Dict] = []
    github_stats: Optional[Dict] = None

class JobRequirement(BaseModel):
    skill: str
    importance: float

class Job(BaseModel):
    title: str
    company: str
    location: Optional[str] = "Not specified"
    description: Optional[str] = None
    requirements: List[Dict]
    url: Optional[str] = None

class SkillMatch(BaseModel):
    skill: str
    job_importance: float
    candidate_level: float
    match_score: float

class MatchResult(BaseModel):
    profile_name: str
    job_title: str
    company: str
    overall_match: float
    skill_matches: List[SkillMatch]
    missing_skills: List[str]
    strengths: List[str]
    recommendation: str

class MatchRequest(BaseModel):
    profile: Profile
    job: Job

@router.post("/profile-job", response_model=MatchResult)
async def match_profile_job(match_request: MatchRequest):
    """
    Match a profile against a job description
    """
    try:
        # Process the match
        match_result = await match_profile_to_job(match_request.profile, match_request.job)

        if not match_result:
            raise HTTPException(status_code=500, detail="Failed to match profile to job")

        return match_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching profile to job: {str(e)}")

@router.post("/batch-match", response_model=List[Dict])
async def batch_match(profiles: List[Profile], jobs: List[Job]):
    """
    Match multiple profiles against multiple jobs
    """
    try:
        results = []
        for profile in profiles:
            profile_matches = []
            for job in jobs:
                match_result = await match_profile_to_job(profile, job)
                profile_matches.append(match_result)

            # Sort matches by score
            profile_matches.sort(key=lambda x: x["overall_match"], reverse=True)

            results.append({
                "profile_name": profile.name,
                "matches": profile_matches
            })

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch matching: {str(e)}")