from app.db.errors.common import EntityDoesNotExistError
from app.db.queries.users import (
    CREATE_USER_QUERY_RETURNING_ID,
    GET_USER_BY_ID,
    GET_USER_BY_USERNAME,
)
from app.db.repositories.base import BaseRepository
from app.models.schemas.users import UserInDB


class UsersRepository(BaseRepository):
    async def create_user(self, *, username: str, password: str) -> UserInDB:
        user = UserInDB(username=username, password=password)
        user.change_password(password)
        id_record = await self._conn.fetchrow(
            CREATE_USER_QUERY_RETURNING_ID, user.username, user.password
        )
        id = id_record.get("id", None)
        user.id = id

        return user

    async def get_user_by_id(self, *, id: int) -> UserInDB:
        user_row = await self._conn.fetchrow(GET_USER_BY_ID, id)
        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExistError(f"A user with id: {id} does not exist")

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_row = await self._conn.fetchrow(GET_USER_BY_USERNAME, username)

        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExistError(f"A user with username {username} does not exist")