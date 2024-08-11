from app.db.errors.common import EntityDoesNotExistError
from app.db.repositories.users import UsersRepository


async def check_username_is_taken(repo: UsersRepository, username: str) -> bool:
    try:
        await repo.get_user_by_username(username=username)
    except EntityDoesNotExistError:
        return False

    return True