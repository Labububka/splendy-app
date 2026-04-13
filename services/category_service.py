from fastapi import HTTPException
import repositories.category_repository as category_repo


def get_all(user_id: str):
    return category_repo.find_all_for_user(user_id)


def create(name: str, user_id: str):
    return category_repo.create(name, user_id)


def delete(category_id: str, user_id: str):
    category = category_repo.find_by_id_and_user(category_id, user_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found or is a default category")
    category_repo.delete(category_id)