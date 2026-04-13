from datetime import date
from fastapi import HTTPException
import repositories.expense_repository as expense_repo


def get_all(user_id: int, date_from=None, date_to=None, category_id=None):
    return expense_repo.find_all(user_id, date_from, date_to, category_id)


def create(user_id: int, amount: float, category_id: int, note: str, date_str: str):
    expense_date = date_str or date.today().isoformat()
    return expense_repo.create(user_id, amount, category_id, note, expense_date)


def update(expense_id: int, user_id: int, fields: dict):
    expense = expense_repo.find_by_id_and_user(expense_id, user_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    cleaned = {k: v for k, v in fields.items() if v is not None}
    if cleaned:
        expense_repo.update(expense_id, cleaned)
    return expense_repo.find_by_id(expense_id)


def delete(expense_id: int, user_id: int):
    expense = expense_repo.find_by_id_and_user(expense_id, user_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense_repo.delete(expense_id)
