from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

MAX_EXPENSE_AMOUNT = 1_000_000
MAX_NOTE_LENGTH = 255


class ExpenseCreate(BaseModel):
    amount: float
    category_id: Optional[int] = None
    note: Optional[str] = None
    date: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_valid(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        if v > MAX_EXPENSE_AMOUNT:
            raise ValueError(f"Amount must be at most {MAX_EXPENSE_AMOUNT}")
        return round(v, 2)

    @field_validator("category_id")
    @classmethod
    def category_id_valid(cls, v):
        if v is not None and v <= 0:
            raise ValueError("category_id must be a positive integer")
        return v

    @field_validator("note")
    @classmethod
    def note_valid(cls, v):
        if v is not None and len(v.strip()) > MAX_NOTE_LENGTH:
            raise ValueError(f"Note must be at most {MAX_NOTE_LENGTH} characters")
        return v.strip() if v else v

    @field_validator("date")
    @classmethod
    def date_valid(cls, v):
        if v is not None:
            try:
                parsed = date.fromisoformat(v)
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
            if parsed > date.today():
                raise ValueError("Date cannot be in the future")
        return v


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category_id: Optional[int] = None
    note: Optional[str] = None
    date: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_valid(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("Amount must be greater than 0")
            if v > MAX_EXPENSE_AMOUNT:
                raise ValueError(f"Amount must be at most {MAX_EXPENSE_AMOUNT}")
            return round(v, 2)
        return v

    @field_validator("category_id")
    @classmethod
    def category_id_valid(cls, v):
        if v is not None and v <= 0:
            raise ValueError("category_id must be a positive integer")
        return v

    @field_validator("note")
    @classmethod
    def note_valid(cls, v):
        if v is not None and len(v.strip()) > MAX_NOTE_LENGTH:
            raise ValueError(f"Note must be at most {MAX_NOTE_LENGTH} characters")
        return v.strip() if v else v

    @field_validator("date")
    @classmethod
    def date_valid(cls, v):
        if v is not None:
            try:
                parsed = date.fromisoformat(v)
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
            if parsed > date.today():
                raise ValueError("Date cannot be in the future")
        return v
