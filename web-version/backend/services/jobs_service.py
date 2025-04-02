from typing import Dict, List

def process_job_requirements(title: str, company: str, skills_text: str, location: str = "Not specified") -> Dict:
    """
    Process job requirements from a text input.

    Args:
        title: Job title
        company: Company name
        skills_text: Comma-separated skills
        location: Job location

    Returns:
        Dict: Processed job data
    """
    # Process skills and assign importance
    skills = []
    for i, skill in enumerate(skills_text.split(",")):
        skill = skill.strip()
        if skill:
            # Assign higher importance to skills listed first
            importance = max(0.3, 1.0 - (i * 0.1))
            skills.append({
                "skill": skill,
                "importance": round(importance, 1)
            })

    # Create job description
    job = {
        "title": title,
        "company": company,
        "location": location,
        "description": f"Custom job description for {title} at {company}",
        "requirements": skills,
        "url": "",  # No URL for manually entered jobs
    }

    return job