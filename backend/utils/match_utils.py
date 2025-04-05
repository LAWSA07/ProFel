from typing import Dict, List, Set, Tuple
import re
from .jobs_utils import normalize_skill_name


def compute_match_score(
    profile_skills: List[Dict],
    job_skills: List[Dict],
    skill_match_threshold: float = 0.7
) -> Dict:
    """
    Compute match score between profile skills and job requirements.

    Args:
        profile_skills: List of skills from a profile
        job_skills: List of skills from a job
        skill_match_threshold: Threshold for skill name similarity (0.0-1.0)

    Returns:
        Dict: Match information including scores, matches, and missing skills
    """
    if not profile_skills or not job_skills:
        return {
            "overall_match": 0.0,
            "skill_matches": [],
            "missing_skills": [skill["name"] for skill in job_skills],
            "strengths": []
        }

    # Initialize results
    skill_matches = []
    missing_skills = []

    # Normalize profile skills for better matching
    profile_skill_names = {
        normalize_skill_name(skill.get("name", "")): skill
        for skill in profile_skills
        if "name" in skill and skill.get("name", "")
    }

    # Normalize job skills
    normalized_job_skills = [
        {
            "name": skill.get("name", ""),
            "normalized_name": normalize_skill_name(skill.get("name", "")),
            "importance": skill.get("importance", 0.5)
        }
        for skill in job_skills
        if "name" in skill and skill.get("name", "")
    ]

    # Total possible score (weighted by importance)
    total_importance = sum(skill.get("importance", 0.5) for skill in normalized_job_skills)

    # Current match score
    current_score = 0.0

    # Process each job skill
    for job_skill in normalized_job_skills:
        job_skill_name = job_skill["normalized_name"]
        importance = job_skill.get("importance", 0.5)

        # Perfect match (exact match after normalization)
        if job_skill_name in profile_skill_names:
            profile_skill = profile_skill_names[job_skill_name]
            match_score = 1.0
            skill_matches.append({
                "skill_name": job_skill["name"],
                "importance": importance,
                "match_score": match_score,
                "weighted_score": importance * match_score
            })
            current_score += importance * match_score
            continue

        # Check for similar matches (partial matches)
        best_match = None
        best_score = 0.0

        for profile_skill_name, profile_skill in profile_skill_names.items():
            # Skip empty skill names
            if not profile_skill_name or not job_skill_name:
                continue

            # Simple token-based matching
            # Calculate percentage of shared tokens
            job_tokens = set(job_skill_name.split())
            profile_tokens = set(profile_skill_name.split())

            # Count shared tokens
            if job_tokens and profile_tokens:
                shared_tokens = job_tokens.intersection(profile_tokens)
                max_tokens = max(len(job_tokens), len(profile_tokens))

                if max_tokens > 0:
                    token_similarity = len(shared_tokens) / max_tokens

                    # Check if this is the best match so far
                    if token_similarity > best_score:
                        best_score = token_similarity
                        best_match = profile_skill

        # If we found a match above the threshold, use it
        if best_match and best_score >= skill_match_threshold:
            skill_matches.append({
                "skill_name": job_skill["name"],
                "importance": importance,
                "match_score": best_score,
                "weighted_score": importance * best_score
            })
            current_score += importance * best_score
        else:
            # No match found
            missing_skills.append(job_skill["name"])

    # Calculate overall match percentage
    overall_match = (current_score / total_importance * 100) if total_importance > 0 else 0.0

    # Identify strengths (high-matching important skills)
    strengths = [
        match["skill_name"]
        for match in skill_matches
        if match["importance"] >= 0.7 and match["match_score"] >= 0.8
    ]

    # Round overall match to nearest integer
    overall_match = round(overall_match)

    return {
        "overall_match": overall_match,
        "skill_matches": skill_matches,
        "missing_skills": missing_skills,
        "strengths": strengths
    }


def generate_recommendation(match_percentage: float) -> str:
    """
    Generate a recommendation based on match percentage.

    Args:
        match_percentage: The overall match percentage (0-100)

    Returns:
        str: Recommendation text
    """
    if match_percentage >= 85:
        return "Excellent Match: This candidate has most of the required skills and would be an excellent fit for this position."
    elif match_percentage >= 70:
        return "Good Match: This candidate has many of the required skills and would likely be a good fit with some training."
    elif match_percentage >= 50:
        return "Moderate Match: This candidate has some of the required skills but may need significant training or may not be ideal for this specific role."
    elif match_percentage >= 30:
        return "Weak Match: This candidate is missing many critical skills required for this position."
    else:
        return "Poor Match: This candidate does not appear to have the necessary skills for this position."


def extract_profile_skills(profile: Dict) -> List[Dict]:
    """
    Extract skills from a profile, handling different formats.

    Args:
        profile: Profile data dictionary

    Returns:
        List[Dict]: Normalized list of skills
    """
    skills = []

    # Handle different ways skills might be stored in the profile
    if "skills" in profile:
        profile_skills = profile["skills"]

        # Case 1: Skills as a list of strings
        if isinstance(profile_skills, list):
            for skill in profile_skills:
                if isinstance(skill, str):
                    skills.append({"name": skill})
                elif isinstance(skill, dict) and "name" in skill:
                    skills.append(skill)

    # Check projects for additional skills
    if "projects" in profile and isinstance(profile["projects"], list):
        for project in profile["projects"]:
            if isinstance(project, dict) and "technologies" in project:
                tech_list = project["technologies"]
                if isinstance(tech_list, list):
                    for tech in tech_list:
                        if isinstance(tech, str):
                            # Check if this skill is already in our list
                            normalized_tech = normalize_skill_name(tech)
                            if not any(normalize_skill_name(s.get("name", "")) == normalized_tech for s in skills):
                                skills.append({"name": tech})

    return skills


def extract_job_skills(job: Dict) -> List[Dict]:
    """
    Extract skills from a job, handling different formats.

    Args:
        job: Job data dictionary

    Returns:
        List[Dict]: Normalized list of skills with importance
    """
    skills = []

    # Handle different ways skills might be stored in the job
    if "skills" in job:
        job_skills = job["skills"]

        # Case 1: Skills as a list of dictionaries with name/importance
        if isinstance(job_skills, list):
            for skill in job_skills:
                if isinstance(skill, dict) and "name" in skill:
                    # Use the skill as-is if it already has importance
                    if "importance" in skill:
                        skills.append(skill)
                    else:
                        # Add default importance
                        skills.append({
                            "name": skill["name"],
                            "importance": 0.5
                        })
                elif isinstance(skill, str):
                    # String skills get default importance
                    skills.append({
                        "name": skill,
                        "importance": 0.5
                    })

    return skills