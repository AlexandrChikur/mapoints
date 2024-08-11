from typing import Any, Optional, Union

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from starlette import status

from app.api.dependencies.auth import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.core.config import settings 
from app.db.errors.common import EntityDoesNotExistError, PointsCapacityReachedMaxValueError
from app.db.errors.points import PointsCapacityReachedError
from app.db.repositories.points import PointsRepository
from app.models.schemas.points import Point, PointInCreate, PointInDB, PointsInResponse, PointFullData
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
    try:
        point = await points_repo.create_point(**point_with_user_id.dict())
    except PointsCapacityReachedMaxValueError:
         raise PointsCapacityReachedError
     
    return point


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PointsInResponse,
    summary="Get all points",
)
async def get_all_points(
    only_ids: Optional[bool] = False,
    lookup: Optional[str] = None,
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> PointsInResponse:
    points = None

    if only_ids:
        points = await points_repo.get_all_points_ids()
        return points

    points = await points_repo.get_all_points(lookup=lookup)

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
    response_model=Union[PointFullData, Any],
    summary="Get point by ID",
)
async def get_point_by_id(
    id: int,
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> Union[PointFullData, Any]:
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
    response_model=Union[PointFullData, Any],
    summary="Get point by ID that user creates",
    dependencies=[Depends(get_current_user_authorizer())],
)
async def get_point_user_by_id(
    id: int,
    current_user: UserInDB = Depends(get_current_user_authorizer()),
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> Union[PointFullData, Any]:
    try:
        point = await points_repo.get_point_by_id(id=id)
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.NOT_FOUND_MESSAGE
        )

    # TODO: get_point_user_by_id & delete_point_user_by_id have same point owner checking -> fix.
    if point.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.OWN_PERMISSION_DENIED,
        )

    return point

@router.delete(
    "/my/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Union[PointFullData, Any],
    summary="Delete point by ID that user creates",
    dependencies=[Depends(get_current_user_authorizer())],
)
async def delete_point_user_by_id(
    id: int,
    current_user: UserInDB = Depends(get_current_user_authorizer()),
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> Union[PointFullData, Any]:
    try:
        point = await points_repo.get_point_by_id(id=id)
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.NOT_FOUND_MESSAGE
        )

    # TODO: get_point_user_by_id & delete_point_user_by_id have same point owner checking -> fix.
    if point.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.OWN_PERMISSION_DENIED,
        )
        
    await points_repo.delete_point_by_id(id=id, owner_id=current_user.id)
    
    return point