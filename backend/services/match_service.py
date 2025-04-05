from typing import Dict, List, Any
import asyncio
from utils.skill_utils import normalize_skill_name

async def match_profile_to_job(profile: Dict, job: Dict) -> Dict:
    """
    Match a profile to a job based on skills.

    Args:
        profile: The profile data
        job: The job data

    Returns:
        Dict: Match result
    """
    # Track skill matches
    skill_matches = []
    total_importance = sum(req["importance"] for req in job["requirements"])
    match_score = 0.0

    # Check each job requirement against profile skills
    for req in job["requirements"]:
        highest_match = 0.0
        candidate_level = 0.0

        # Normalize job requirement skill
        req_skill_norm = normalize_skill_name(req["skill"])

        # Check against each profile skill
        for skill_obj in profile["skills"]:
            # Get skill name from either format
            skill_name = skill_obj.get("name", skill_obj) if isinstance(skill_obj, dict) else skill_obj

            # Normalize profile skill
            skill_norm = normalize_skill_name(skill_name)

            # Check for match or partial match
            if (skill_norm == req_skill_norm or
                req_skill_norm in skill_norm or
                skill_norm in req_skill_norm):

                # Calculate match based on skill level if available
                skill_level = 1.0  # Default full match
                if isinstance(skill_obj, dict) and "level" in skill_obj:
                    if skill_obj["level"].lower() in ["expert", "advanced"]:
                        skill_level = 1.0
                    elif skill_obj["level"].lower() in ["intermediate"]:
                        skill_level = 0.7
                    elif skill_obj["level"].lower() in ["beginner", "basic"]:
                        skill_level = 0.4

                # Calculate match value based on importance
                match_value = req["importance"] * skill_level

                # Keep track of highest match
                if match_value > highest_match:
                    highest_match = match_value
                    candidate_level = skill_level

        # Add to total match score
        match_score += highest_match

        # Create skill match object
        skill_matches.append({
            "skill": req["skill"],
            "job_importance": req["importance"],
            "candidate_level": candidate_level,
            "match_score": highest_match
        })

    # Calculate overall match percentage
    overall_match = (match_score / total_importance) * 100 if total_importance > 0 else 0

    # Find missing skills (those with zero match score)
    missing_skills = [
        match["skill"] for match in skill_matches
        if match["match_score"] == 0
    ]

    # Find strengths (skills with high match scores)
    strengths = [
        match["skill"] for match in skill_matches
        if match["match_score"] >= 0.7 * match["job_importance"] and match["match_score"] > 0
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
    return {
        "profile_name": profile["name"],
        "job_title": job["title"],
        "company": job["company"],
        "overall_match": overall_match,
        "skill_matches": skill_matches,
        "missing_skills": missing_skills,
        "strengths": strengths,
        "recommendation": recommendation
    }