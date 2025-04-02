import csv
import json
from typing import Dict, List, Set, Any

from models.profile import Profile
from models.job import JobListing
from models.match import ProfileJobMatch


def is_duplicate_venue(venue_name: str, seen_names: set) -> bool:
    """Legacy function for venue data, kept for compatibility"""
    return venue_name in seen_names


def is_complete_venue(venue: dict, required_keys: list) -> bool:
    """Legacy function for venue data, kept for compatibility"""
    return all(key in venue for key in required_keys)


def save_venues_to_csv(venues: list, filename: str):
    """Legacy function for venue data, kept for compatibility"""
    if not venues:
        print("No venues to save.")
        return

    # Use field names from the first venue as a fallback
    fieldnames = venues[0].keys() if venues else []

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(venues)
    print(f"Saved {len(venues)} venues to '{filename}'.")


def save_to_json(data: Any, filename: str) -> None:
    """
    Save data to a JSON file.

    Args:
        data: The data to save
        filename: Path to the output file
    """
    with open(filename, 'w', encoding='utf-8') as f:
        # Convert Pydantic models to dicts before serialization
        if isinstance(data, (Profile, JobListing, ProfileJobMatch)):
            # Use model_dump() for Pydantic v2 models
            if hasattr(data, 'model_dump'):
                json_data = data.model_dump()
            # Fallback for older Pydantic versions
            elif hasattr(data, 'dict'):
                json_data = data.dict()
            else:
                json_data = data
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        elif isinstance(data, list):
            # Handle lists that might contain Pydantic models
            serialized_list = []
            for item in data:
                if hasattr(item, 'model_dump'):
                    serialized_list.append(item.model_dump())
                elif hasattr(item, 'dict'):
                    serialized_list.append(item.dict())
                else:
                    serialized_list.append(item)
            json.dump(serialized_list, f, indent=2, ensure_ascii=False)
        else:
            # For regular dictionaries or other JSON-serializable objects
            json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved data to '{filename}'")


def load_from_json(filename: str) -> Any:
    """
    Load data from a JSON file.

    Args:
        filename: Path to the input file

    Returns:
        The loaded data
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename}: {e}")
        return None


def normalize_skill_name(skill: str) -> str:
    """
    Normalize skill names to handle variations.

    Args:
        skill: The skill name to normalize

    Returns:
        Normalized skill name
    """
    # Convert to lowercase
    normalized = skill.lower()

    # Handle common variations
    replacements = {
        "javascript": ["js", "ecmascript"],
        "typescript": ["ts"],
        "python": ["py"],
        "react": ["reactjs", "react.js"],
        "node.js": ["nodejs", "node"],
        "c#": ["csharp", "c sharp"],
        "c++": ["cpp", "cplusplus"],
        "postgresql": ["postgres"],
        "machine learning": ["ml"],
        "artificial intelligence": ["ai"],
    }

    # Check if the skill should be normalized
    for standard, variations in replacements.items():
        if normalized in variations:
            return standard

    return normalized
