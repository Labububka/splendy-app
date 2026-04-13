from fastapi import APIRouter, Depends
from auth_helpers import get_current_user
from dtos.category_dto import CategoryCreate
import services.category_service as category_service

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def get_categories(user_id: int = Depends(get_current_user)):
    return category_service.get_all(user_id)


@router.post("", status_code=201)
def create_category(body: CategoryCreate, user_id: int = Depends(get_current_user)):
    return category_service.create(body.name, user_id)


@router.delete("/{category_id}")
def delete_category(category_id: int, user_id: int = Depends(get_current_user)):
    category_service.delete(category_id, user_id)
    return {"message": "Deleted"}
