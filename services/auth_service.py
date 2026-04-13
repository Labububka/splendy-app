import sqlite3
from fastapi import HTTPException
from auth_helpers import hash_password, create_token
import repositories.user_repository as user_repo


def register(email: str, password: str, name: str):
    try:
        user_repo.create(email, hash_password(password), name)
        user = user_repo.find_by_email(email)
        return {"token": create_token(user["id"])}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")


def login(email: str, password: str):
    user = user_repo.find_by_email_and_password(email, hash_password(password))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_token(user["id"])}
