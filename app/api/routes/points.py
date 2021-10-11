from typing import List, Optional

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
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> PointsInResponse:
    return await points_repo.get_all_points()
