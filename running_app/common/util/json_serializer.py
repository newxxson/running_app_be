from enum import StrEnum
import json
from typing import Any

from pydantic import BaseModel


def is_json_serializable(obj: Any) -> bool:
    """Checks if object is json serializable."""
    try:
        json.dumps(obj)
    except (TypeError, OverflowError):
        return False

    return True


def convert_to_serializable(obj: Any) -> Any:
    """Changes dict to json serializable."""
    if isinstance(obj, dict):
        # Recursively convert each value in the dictionary.
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        # Recursively convert each item in the list.
        return [convert_to_serializable(item) for item in obj]
    if isinstance(obj, BaseModel):
        # Convert Pydantic models to dictionaries.
        return convert_to_serializable(obj.model_dump())
    if isinstance(obj, StrEnum):
        return str(obj)
    if hasattr(obj, "__dict__"):
        # 일반 클래스 변환
        attributes = [
            attr
            for attr in dir(obj)
            if not callable(getattr(obj, attr)) and not attr.startswith("__")
        ]
        return {
            attr: convert_to_serializable(getattr(obj, attr)) for attr in attributes
        }
    return str(obj) if obj else obj
