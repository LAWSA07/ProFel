from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict
import asyncio

from services.github_service import process_github_profile

router = APIRouter()

class GitHubProfileRequest(BaseModel):
    username: str

class ProfileResponse(BaseModel):
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    skills: List[Dict]
    projects: List[Dict] = []
    github_stats: Optional[Dict] = None

@router.post("/profile", response_model=ProfileResponse)
async def get_github_profile(profile_request: GitHubProfileRequest):
    """
    Get GitHub profile data for a username
    """
    try:
        # Extract username and handle URLs
        username = profile_request.username
        if "github.com/" in username:
            parts = username.split("github.com/")
            if len(parts) > 1:
                username = parts[1].strip().split("/")[0].split("?")[0]
            else:
                raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        # Process the profile
        profile_data = await process_github_profile(username)

        if not profile_data:
            raise HTTPException(status_code=404, detail=f"GitHub profile not found: {username}")

        return profile_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing GitHub profile: {str(e)}")