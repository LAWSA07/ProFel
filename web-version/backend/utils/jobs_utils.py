import re
from typing import List, Dict, Tuple


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract skills from job description text.

    Args:
        text: Text containing skills

    Returns:
        List[str]: Extracted skills
    """
    if not text:
        return []

    # Split by common separators (comma, semicolon, newline, bullet points)
    raw_skills = re.split(r'[,;\n•]+', text)

    # Clean and filter empty skills
    skills = []
    for skill in raw_skills:
        # Basic cleaning
        cleaned = skill.strip().strip('.')
        if cleaned and len(cleaned) > 1:  # Minimum 2 characters
            skills.append(cleaned)

    return skills


def normalize_skill_name(skill_name: str) -> str:
    """
    Normalize skill names for better matching.

    Args:
        skill_name: Name of the skill to normalize

    Returns:
        str: Normalized skill name
    """
    if not skill_name:
        return ""

    # Convert to lowercase
    normalized = skill_name.lower()

    # Remove common prefixes/suffixes
    normalized = re.sub(r'^(knowledge of|experience with|proficiency in|skills in|understanding of)\s+', '', normalized)
    normalized = re.sub(r'\s+(basics|fundamentals|framework|library|development|programming|language)$', '', normalized)

    # Replace alternative names with canonical ones
    replacements = {
        r'\bjs\b': 'javascript',
        r'\bts\b': 'typescript',
        r'\bpy\b': 'python',
        r'\bnodejs\b': 'node.js',
        r'\breact\s*js\b': 'react',
        r'\bangular\s*js\b': 'angular',
        r'\bvue\s*js\b': 'vue',
        r'\bc\s*\+\+\b': 'c++',
        r'\bc\s*\#\b': 'c#',
        r'\b\.net\s+core\b': '.net core',
        r'\bazure\s+devops\b': 'azure devops',
        r'\baws\s+services\b': 'aws',
        r'\bcloud\s+technologies\b': 'cloud computing',
        r'\brest\s+api\b': 'rest',
        r'\bml\b': 'machine learning',
        r'\bai\b': 'artificial intelligence',
        r'\bnlp\b': 'natural language processing',
        r'\bdata\s+science\b': 'data science',
        r'\bdb\b': 'database',
        r'\brdbms\b': 'relational database',
        r'\bsql\s+database\b': 'sql',
        r'\bgcp\b': 'google cloud platform',
        r'\bnosql\s*databases?\b': 'nosql',
        r'\boop\b': 'object-oriented programming',
        r'\bfp\b': 'functional programming',
        r'\bui/ux\b': 'ui/ux design',
        r'\bui\b': 'user interface',
        r'\bux\b': 'user experience',
    }

    for pattern, replacement in replacements.items():
        normalized = re.sub(pattern, replacement, normalized)

    # Remove common stop words
    stop_words = ['the', 'and', 'or', 'a', 'an', 'in', 'on', 'with', 'using', 'for', 'to']
    normalized_parts = normalized.split()
    normalized_parts = [word for word in normalized_parts if word not in stop_words]
    normalized = ' '.join(normalized_parts)

    # Trim
    normalized = normalized.strip()

    return normalized


def calculate_skill_importance(skills: List[str], position: int, total_skills: int) -> float:
    """
    Calculate the importance of a skill based on its position in the skills list.
    Earlier skills are typically more important.

    Args:
        skills: List of all skills
        position: Position of the skill in the list (0-based)
        total_skills: Total number of skills

    Returns:
        float: Importance score between 0.1 and 1.0
    """
    if not skills or position >= len(skills) or total_skills == 0:
        return 0.5  # Default mid-importance

    # Skills mentioned earlier are more important
    # Use a non-linear curve to weight early skills higher
    if total_skills == 1:
        return 1.0

    # Calculate importance on a scale from 1.0 to 0.1
    min_importance = 0.1
    importance = 1.0 - ((1.0 - min_importance) * position / (total_skills - 1))

    # Round to one decimal place
    return round(importance, 1)


def calculate_job_level(title: str) -> str:
    """
    Calculate the level of the job position from the title.

    Args:
        title: Job title

    Returns:
        str: Job level (entry, mid, senior)
    """
    title_lower = title.lower()

    # Check for senior-level indicators
    if any(term in title_lower for term in ['senior', 'sr', 'lead', 'principal', 'staff', 'architect', 'manager', 'head', 'chief', 'cto', 'vp']):
        return "senior"

    # Check for junior-level indicators
    if any(term in title_lower for term in ['junior', 'jr', 'entry', 'intern', 'trainee', 'graduate', 'associate']):
        return "entry"

    # Default to mid-level
    return "mid"


def generate_job_description(title: str, company: str, skills: List[str], location: str = "Remote") -> str:
    """
    Generate a standardized job description.

    Args:
        title: Job title
        company: Company name
        skills: List of required skills
        location: Job location

    Returns:
        str: Generated job description
    """
    level = calculate_job_level(title)

    # Create job description intro based on level
    if level == "entry":
        intro = f"{company} is looking for an entry-level {title} to join our team."
        experience = "This is an excellent opportunity for recent graduates or developers early in their career path."
    elif level == "senior":
        intro = f"{company} is seeking an experienced {title} to lead our technical initiatives."
        experience = "The ideal candidate will have extensive experience and can mentor junior team members."
    else:  # mid-level
        intro = f"{company} is hiring a {title} to strengthen our development team."
        experience = "We're looking for someone with proven experience who can hit the ground running."

    # Format skills section
    if skills:
        # Take top 5 skills for the description
        top_skills = skills[:min(5, len(skills))]
        skills_text = ", ".join(top_skills)
        skills_section = f"Key technologies include {skills_text}, among others."
    else:
        skills_section = "Experience with relevant technologies is required."

    # Combine sections
    description = f"{intro} {experience} {skills_section} This position is located in {location}."

    return description