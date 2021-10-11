from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.dependencies.database import get_repository
from app.db.repositories.points import PointsRepository
from app.models.schemas.points import Point, PointInDB, PointsInResponse

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=Point,
    summary="Create Point",
)
async def create_point(
    point_create: Point = Body(..., alias="point"),
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> PointInDB:
    point = await points_repo.create_point(**point_create.dict())
    return point


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PointsInResponse,
    summary="Get all points",
)
async def get_all_points(
    only_uids: Optional[bool] = False,
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> PointsInResponse:
    if only_uids:
        return await points_repo.get_all_points_uids()
    return await points_repo.get_all_points()


@router.get(
    "/{uid}",
    status_code=status.HTTP_200_OK,
    response_model=PointInDB,
    summary="Get point by UID",
)
async def get_all_points(
    uid: UUID,
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> PointInDB:
    return await points_repo.get_point_by_uid(uid=uid)
