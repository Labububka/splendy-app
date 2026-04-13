from datetime import date
from fastapi import HTTPException
import repositories.expense_repository as expense_repo
import repositories.category_repository as category_repo


def get_all(user_id: str, date_from=None, date_to=None, category_id=None):
    if date_from and date_to and date_from > date_to:
        raise HTTPException(status_code=400, detail="date_from must be before date_to")
    return expense_repo.find_all(user_id, date_from, date_to, category_id)


def create(user_id: str, amount: float, category_id: str, note: str, date_str: str):
    if category_id is not None:
        category = category_repo.find_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    expense_date = date_str or date.today().isoformat()
    return expense_repo.create(user_id, amount, category_id, note, expense_date)


def update(expense_id: str, user_id: str, fields: dict):
    expense = expense_repo.find_by_id_and_user(expense_id, user_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if fields.get("category_id") is not None:
        category = category_repo.find_by_id(fields["category_id"])
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    cleaned = {k: v for k, v in fields.items() if v is not None}
    if cleaned:
        expense_repo.update(expense_id, cleaned)
    return expense_repo.find_by_id(expense_id)


def delete(expense_id: str, user_id: str):
    expense = expense_repo.find_by_id_and_user(expense_id, user_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense_repo.delete(expense_id)
