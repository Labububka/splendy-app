from fastapi import APIRouter, Depends
from typing import Optional
from auth_helpers import get_current_user
from dtos.expense_dto import ExpenseCreate, ExpenseUpdate
import services.expense_service as expense_service

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("")
def get_expenses(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    category_id: Optional[str] = None,
    user_id: str = Depends(get_current_user)
):
    return expense_service.get_all(user_id, date_from, date_to, category_id)


@router.post("", status_code=201)
def create_expense(body: ExpenseCreate, user_id: str = Depends(get_current_user)):
    return expense_service.create(user_id, body.amount, body.category_id, body.note, body.date)


@router.put("/{expense_id}")
def update_expense(expense_id: str, body: ExpenseUpdate, user_id: str = Depends(get_current_user)):
    return expense_service.update(expense_id, user_id, body.model_dump())


@router.delete("/{expense_id}")
def delete_expense(expense_id: str, user_id: str = Depends(get_current_user)):
    expense_service.delete(expense_id, user_id)
    return {"message": "Deleted"}
