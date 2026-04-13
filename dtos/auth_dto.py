import re
from pydantic import BaseModel, field_validator
from constants import MIN_NAME_LENGTH, MAX_NAME_LENGTH

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
PASSWORD_UPPERCASE_REGEX = r"[A-Z]"
PASSWORD_DIGIT_REGEX = r"\d"
MIN_PASSWORD_LENGTH = 8


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

    @field_validator("email")
    @classmethod
    def email_valid(cls, v):
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Invalid email format")
        return v.lower().strip()

    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        if len(v) < MIN_PASSWORD_LENGTH:
            raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
        if not re.search(PASSWORD_UPPERCASE_REGEX, v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(PASSWORD_DIGIT_REGEX, v):
            raise ValueError("Password must contain at least one digit")
        return v

    @field_validator("name")
    @classmethod
    def name_valid(cls, v):
        if len(v.strip()) < MIN_NAME_LENGTH:
            raise ValueError(f"Name must be at least {MIN_NAME_LENGTH} characters")
        if len(v.strip()) > MAX_NAME_LENGTH:
            raise ValueError(f"Name must be at most {MAX_NAME_LENGTH} characters")
        return v.strip()


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def email_valid(cls, v):
        if not v or not v.strip():
            raise ValueError("Email is required")
        return v.lower().strip()

    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        if not v or not v.strip():
            raise ValueError("Password is required")
        return v
