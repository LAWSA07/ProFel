from typing import List, Dict, Optional
import asyncio

from models.profile import Profile, Skill
from models.job import JobListing, JobRequirement
from models.match import ProfileJobMatch, SkillMatch
from utils.data_utils import normalize_skill_name


async def match_profile_to_job(
    profile: Profile,
    job: JobListing
) -> ProfileJobMatch:
    """
    Match a candidate profile to a job listing.

    Args:
        profile: The candidate profile
        job: The job listing

    Returns:
        ProfileJobMatch: The match result
    """
    # Track skill matches
    skill_matches = []
    total_importance = sum(req.importance for req in job.requirements)
    match_score = 0.0

    # Check each job requirement against profile skills
    for req in job.requirements:
        highest_match = 0.0
        candidate_level = 0.0

        # Normalize job requirement skill
        req_skill_norm = normalize_skill_name(req.skill)

        # Check against each profile skill
        for skill in profile.skills:
            # Normalize profile skill
            skill_norm = normalize_skill_name(skill.name)

            # Check for match or partial match
            if (skill_norm == req_skill_norm or
                req_skill_norm in skill_norm or
                skill_norm in req_skill_norm):

                # Calculate match based on skill level if available
                skill_level = 1.0  # Default full match
                if skill.level:
                    if skill.level.lower() in ["expert", "advanced"]:
                        skill_level = 1.0
                    elif skill.level.lower() in ["intermediate"]:
                        skill_level = 0.7
                    elif skill.level.lower() in ["beginner", "basic"]:
                        skill_level = 0.4

                # Calculate match value based on importance
                match_value = req.importance * skill_level

                # Keep track of highest match
                if match_value > highest_match:
                    highest_match = match_value
                    candidate_level = skill_level

        # Add to total match score
        match_score += highest_match

        # Create skill match object
        skill_matches.append(SkillMatch(
            skill=req.skill,
            job_importance=req.importance,
            candidate_level=candidate_level,
            match_score=highest_match
        ))

    # Calculate overall match percentage
    overall_match = (match_score / total_importance) * 100 if total_importance > 0 else 0

    # Find missing skills (those with zero match score)
    missing_skills = [
        match.skill for match in skill_matches
        if match.match_score == 0
    ]

    # Find strengths (skills with high match scores)
    strengths = [
        match.skill for match in skill_matches
        if match.match_score >= 0.7 * match.job_importance and match.match_score > 0
    ]

    # Generate recommendation
    if overall_match >= 85:
        recommendation = "Excellent match - Highly recommended for this position"
    elif overall_match >= 70:
        recommendation = "Good match - Strong candidate for this position"
    elif overall_match >= 50:
        recommendation = "Moderate match - Consider with additional training"
    elif overall_match >= 30:
        recommendation = "Weak match - Significant skill gaps for this position"
    else:
        recommendation = "Poor match - Not recommended for this position"

    # Create match result
    return ProfileJobMatch(
        profile_name=profile.name,
        job_title=job.title,
        company=job.company,
        overall_match=overall_match,
        skill_matches=skill_matches,
        missing_skills=missing_skills,
        strengths=strengths,
        recommendation=recommendation
    )


async def batch_match_profiles_to_jobs(
    profiles: List[Profile],
    jobs: List[JobListing]
) -> List[Dict]:
    """
    Match multiple profiles to multiple jobs.

    Args:
        profiles: List of candidate profiles
        jobs: List of job listings

    Returns:
        List[Dict]: Matching results for each profile
    """
    results = []

    for profile in profiles:
        profile_matches = []

        # Match profile to each job
        for job in jobs:
            match = await match_profile_to_job(profile, job)
            profile_matches.append(match)

        # Sort matches by score (descending)
        profile_matches.sort(key=lambda m: m.overall_match, reverse=True)

        # Add to results
        results.append({
            "profile_name": profile.name,
            "matches": [m.model_dump() for m in profile_matches]
        })

    return results