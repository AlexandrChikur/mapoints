from pydantic import BaseModel, validator

from app.models.common import IDModelMixin
from app.services import security


class User(IDModelMixin, BaseModel):
    username: str


class UserInLogin(BaseModel):
    username: str
    password: str


class UserInCreate(UserInLogin):
    pass


class UserWithToken(User):
    token: str


class UserInResponse(BaseModel):
    user: UserWithToken


class UserInDB(User):
    password: str

    def check_password(self, password: str) -> bool:
        return security.verify_password(password, self.password)

    def change_password(self, password: str) -> None:
        self.password = security.get_password_hash(password)
