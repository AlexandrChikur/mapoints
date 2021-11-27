from typing import Any, List, Optional, Union

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from starlette import status

from app.api.dependencies.auth import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors.common import EntityDoesNotExistError
from app.db.repositories.points import PointsRepository
from app.models.schemas.points import (Point, PointInCreate, PointInDB,
                                       PointsInResponse)
from app.models.schemas.users import UserInDB
from app.resources import strings

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PointInDB,
    summary="Create Point",
    dependencies=[Depends(get_current_user_authorizer())],
)
async def create_point(
    point_create: Point = Body(..., alias="point"),
    current_user: UserInDB = Depends(get_current_user_authorizer()),
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> PointInDB:
    point_with_user_id = PointInCreate(**point_create.dict(), user_id=current_user.id)
    point = await points_repo.create_point(**point_with_user_id.dict())
    return point


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PointsInResponse,
    summary="Get all points",
)
async def get_all_points(
    only_ids: Optional[bool] = False,
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> PointsInResponse:
    points = None

    if only_ids:
        points = await points_repo.get_all_points_ids()
        return points

    points = await points_repo.get_all_points()

    return points


@router.get(
    "/my",
    status_code=status.HTTP_200_OK,
    response_model=PointsInResponse,
    summary="Get all points that user creates",
    dependencies=[Depends(get_current_user_authorizer())],
)
async def get_all_user_points(
    current_user: UserInDB = Depends(get_current_user_authorizer()),
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> PointsInResponse:
    points = None

    # means get all points of the user
    points = await points_repo.get_all_points(user_id=current_user.id)

    return points


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Union[PointInDB, Any],
    summary="Get point by ID",
)
async def get_point_by_id(
    id: int,
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> Union[PointInDB, Any]:
    try:
        point = await points_repo.get_point_by_id(id=id)
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.NOT_FOUND_MESSAGE
        )

    return point


@router.get(
    "/my/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Union[PointInDB, Any],
    summary="Get point by ID that user creates",
    dependencies=[Depends(get_current_user_authorizer())],
)
async def get_point_user_by_id(
    id: int,
    current_user: UserInDB = Depends(get_current_user_authorizer()),
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> Union[PointInDB, Any]:
    try:
        point = await points_repo.get_point_by_id(id=id)
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.NOT_FOUND_MESSAGE
        )

    if point.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.NOT_POINT_OWNER_ERROR_MESSAGE,
        )

    return point
