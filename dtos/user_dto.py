from pydantic import BaseModel
from typing import Optional


class UserUpdate(BaseModel):
    name: Optional[str] = None
    currency: Optional[str] = None
    notifications: Optional[bool] = None
