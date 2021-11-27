from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from starlette import status

from app.api.dependencies.database import get_repository
from app.db.errors.common import EntityDoesNotExistError
from app.db.repositories.points import PointsRepository
from app.models.schemas.maps import Map
from app.models.schemas.points import Point, PointInDB, PointsInResponse

router = APIRouter()


@router.get(
    "/routes",
    response_model=List,
    status_code=status.HTTP_200_OK,
    summary="Get all routes of the map",
)
async def get_map_routes(
    points_ids: List[int] = Query(..., alias="points_ids"),
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> List:
    """Returns a list of routes that consists in map of provided points"""
    points = []
    for id in points_ids:
        try:
            point = await points_repo.get_point_by_id(id=id)
        except EntityDoesNotExistError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Point with id: <{id}> not found",
            )
        points.append(point)

    m = Map(points=points)

    return m.routes


@router.get(
    "/routes/best",
    response_model=List,
    status_code=status.HTTP_200_OK,
    summary="Get the best route of all routes",
)
async def get_best_route(
    points_ids: List[int] = Query(..., alias="points_ids"),
    with_total: Optional[bool] = Query(False),
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> List:
    """
    Returns a list with the best route that contains in map of all provided points
    :param with_total: bool - The parameter that add total distance to response (float type)
    """
    points = []
    total_distance = None

    for id in points_ids:
        try:
            point = await points_repo.get_point_by_id(id=id)
        except EntityDoesNotExistError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Point with id: <{id}> not found",
            )
        points.append(point)

    m = Map(points=points)
    best_route = m.get_best_route()

    if with_total:
        total_distance = m.get_total_route_distance(best_route)

    return JSONResponse(
        content={
            "route": best_route,
            "total_distance": total_distance,
        }
    )
