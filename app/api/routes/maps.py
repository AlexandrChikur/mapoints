from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from starlette import status

from app.api.dependencies.auth import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors.common import EntityDoesNotExistError
from app.db.repositories.points import PointsRepository
from app.models.schemas.maps import Map
from app.models.schemas.users import UserInDB

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


@router.get(
    "/my/routes",
    response_model=List,
    status_code=status.HTTP_200_OK,
    summary="Get all routes of the map that contains points that user created",
)
async def get_map_user_routes(
    current_user: UserInDB = Depends(get_current_user_authorizer()),
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> List:
    """Returns all routes of the map that contains points that user created"""
    responsed_points = await points_repo.get_all_points(
        user_id=current_user.id
    )  # Returns points and count of them
    m = Map(points=responsed_points.results)  # Attribute results is a list of points

    return m.routes


@router.get(
    "/my/routes/best",
    response_model=List,
    status_code=status.HTTP_200_OK,
    summary="Get the best route of all user's points",
)
async def get_best_route(
    with_total: Optional[bool] = Query(False),
    current_user: UserInDB = Depends(get_current_user_authorizer()),
    points_repo: PointsRepository = Depends(get_repository(PointsRepository)),
) -> List:
    """
    Returns a list with the best route that contains in map of all points that user created

    :param with_total: bool - The parameter that add total distance to response (float type)
    """
    total_distance = None
    responsed_points = await points_repo.get_all_points(
        user_id=current_user.id
    )  # Returns points and count of them
    m = Map(points=responsed_points.results)  # Attribute results is a list of points
    best_route = m.get_best_route()

    if with_total:
        total_distance = m.get_total_route_distance(best_route)

    return JSONResponse(
        content={
            "route": best_route,
            "total_distance": total_distance,
        }
    )