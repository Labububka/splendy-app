from fastapi import APIRouter, Depends
from auth_helpers import get_current_user
from dtos.user_dto import UserUpdate
import services.user_service as user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me(user_id: int = Depends(get_current_user)):
    return user_service.get_me(user_id)


@router.put("/me")
def update_me(body: UserUpdate, user_id: int = Depends(get_current_user)):
    return user_service.update_me(user_id, body.model_dump())
