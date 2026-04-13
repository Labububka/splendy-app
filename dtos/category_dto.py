from pydantic import BaseModel, field_validator
from constants import DEFAULT_CATEGORIES, MAX_NAME_LENGTH, MIN_NAME_LENGTH


class CategoryCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def name_valid(cls, v):
        if not v or not v.strip():
            raise ValueError("Category name is required")
        if len(v.strip()) < MIN_NAME_LENGTH:
            raise ValueError(f"Category name must be at least {MIN_NAME_LENGTH} characters")
        if len(v.strip()) > MAX_NAME_LENGTH:
            raise ValueError(f"Category name must be at most {MAX_NAME_LENGTH} characters")
        if v.strip().capitalize() in DEFAULT_CATEGORIES:
            raise ValueError("Category already exists as a default")
        return v.strip().capitalize()
