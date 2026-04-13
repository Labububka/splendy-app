import repositories.user_repository as user_repo


def get_me(user_id: str):
    return dict(user_repo.find_by_id(user_id))


def update_me(user_id: str, fields: dict):
    cleaned = {k: v for k, v in fields.items() if v is not None}
    if cleaned:
        user_repo.update(user_id, cleaned)
    return dict(user_repo.find_by_id(user_id))
