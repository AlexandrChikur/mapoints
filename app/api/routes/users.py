from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from app.api.dependencies.database import get_repository
from app.core.config import settings
from app.db.errors.common import EntityDoesNotExistError
from app.db.errors.users import WrongLoginError, WrongUserIdError
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import (
    User,
    UserInCreate,
    UserInDB,
    UserInResponse,
    UserWithToken,
)
from app.resources import strings
from app.services import jwt
from app.services.auth import check_username_is_taken

router = APIRouter()


@router.post(
    "/signup",
    status_code=status.HTTP_200_OK,
    response_model=UserInResponse,
    summary="Create User"
)
async def user_signup(
    user_create: UserInCreate = Body(..., alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    if await check_username_is_taken(users_repo, user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.USERNAME_TAKEN
        )
    user = await users_repo.create_user(**user_create.dict())
    token = jwt.create_access_token_for_user(user, str(settings.SECRET_KEY))

    return UserInResponse(
        user=UserWithToken(id=user.id, username=user.username, token=token)
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=UserInResponse,
    summary="Login User"
)
async def user_login(
    user_login: UserInCreate = Body(..., alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    try:
        user = await users_repo.get_user_by_username(username=user_login.username)
    except EntityDoesNotExistError as existence_error:
        raise WrongLoginError from existence_error

    if not user.check_password(user_login.password):
        raise WrongLoginError

    token = jwt.create_access_token_for_user(user, str(settings.SECRET_KEY))

    return UserInResponse(
        user=UserWithToken(id=user.id, username=user.username, token=token)
    )


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
    summary="Get user by id"
)
async def get_user_by_id(
    id: int = Query(..., title="id", description="user id"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> User:
    try:
        user = await users_repo.get_user_by_id(id=id)
    except EntityDoesNotExistError:
        raise WrongUserIdError
    
    return User(id=user.id, username=user.username)
