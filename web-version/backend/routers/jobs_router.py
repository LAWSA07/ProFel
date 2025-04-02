from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

from services.jobs_service import process_job_requirements

router = APIRouter()

class JobRequirement(BaseModel):
    skill: str
    importance: float

class JobDescription(BaseModel):
    title: str
    company: str
    location: Optional[str] = "Not specified"
    description: Optional[str] = None
    requirements: List[Dict]
    url: Optional[str] = None

@router.post("/parse-job")
async def parse_job_description(job_input: str):
    """
    Parse a job description in the format:
    <job_title> | <company> | <key_skills_comma_separated>
    """
    try:
        parts = job_input.split("|")
        if len(parts) < 3:
            raise HTTPException(status_code=400, detail="Invalid job format. Use: <job_title> | <company> | <key_skills_comma_separated>")

        title = parts[0].strip()
        company = parts[1].strip()
        skills_text = parts[2].strip()

        # Process the job input
        job_data = process_job_requirements(title, company, skills_text,
                                           parts[3].strip() if len(parts) > 3 else "Not specified")

        return job_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing job description: {str(e)}")

@router.post("/create-job", response_model=JobDescription)
async def create_job(job: JobDescription):
    """
    Create a job description with pre-formatted requirements
    """
    try:
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating job description: {str(e)}")