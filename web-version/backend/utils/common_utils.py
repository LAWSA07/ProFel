import os
import uuid
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

def generate_unique_id() -> str:
    """
    Generate a unique identifier.

    Returns:
        str: Unique identifier
    """
    return str(uuid.uuid4())


def timestamp_now() -> str:
    """
    Get current timestamp in ISO format.

    Returns:
        str: Current timestamp
    """
    return datetime.now().isoformat()


def ensure_directory_exists(path: str) -> None:
    """
    Create directory if it doesn't exist.

    Args:
        path: Directory path to ensure exists
    """
    os.makedirs(path, exist_ok=True)


def read_json_file(file_path: str, default: Any = None) -> Any:
    """
    Read and parse JSON file.

    Args:
        file_path: Path to JSON file
        default: Default value if file doesn't exist or is invalid

    Returns:
        Parsed JSON content or default value
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except (json.JSONDecodeError, IOError):
        return default


def write_json_file(file_path: str, data: Any) -> bool:
    """
    Write data to JSON file.

    Args:
        file_path: Path to JSON file
        data: Data to write to file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if directory:
            ensure_directory_exists(directory)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except (TypeError, IOError):
        return False


def merge_dictionaries(dict1: Dict, dict2: Dict, overwrite: bool = True) -> Dict:
    """
    Merge two dictionaries.

    Args:
        dict1: First dictionary
        dict2: Second dictionary
        overwrite: Whether to overwrite values in dict1 with values from dict2

    Returns:
        Dict: Merged dictionary
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = merge_dictionaries(result[key], value, overwrite)
        elif key not in result or overwrite:
            # Add new key or overwrite existing one
            result[key] = value

    return result


def validate_required_fields(data: Dict, required_fields: List[str]) -> List[str]:
    """
    Validate required fields in data.

    Args:
        data: Dictionary to validate
        required_fields: List of required field names

    Returns:
        List[str]: List of missing fields
    """
    missing_fields = []

    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)

    return missing_fields


def format_error_response(message: str, details: Optional[Dict] = None) -> Dict:
    """
    Format a standard error response.

    Args:
        message: Error message
        details: Optional error details

    Returns:
        Dict: Formatted error response
    """
    response = {
        "success": False,
        "error": message,
        "timestamp": timestamp_now(),
    }

    if details:
        response["details"] = details

    return response


def format_success_response(data: Any, message: str = "Operation successful") -> Dict:
    """
    Format a standard success response.

    Args:
        data: Response data
        message: Success message

    Returns:
        Dict: Formatted success response
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": timestamp_now(),
    }