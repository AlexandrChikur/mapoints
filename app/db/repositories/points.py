from typing import Optional

from app.db.errors.common import EntityDoesNotExistError
from app.db.queries.points import *
from app.models.schemas.points import PointIDOnly, PointInDB, PointsInResponse

from .base import BaseRepository


class PointsRepository(BaseRepository):
    async def create_point(
        self, *, name: str, x: int, y: int, user_id: int
    ) -> PointInDB:
        point = PointInDB(name=name, x=x, y=y, user_id=user_id)
        id_record = await self._conn.fetchrow(
            CREATE_POINT_QUERY_RETURNING_ID, point.name, point.x, point.y, user_id
        )
        id = id_record.get("id", None)
        point.id = id

        return point

    async def get_all_points(self, user_id: Optional[int] = None) -> PointsInResponse:
        if user_id:
            points = await self._conn.fetch(GET_ALL_USER_POINTS, user_id)
        else:
            points = await self._conn.fetch(GET_ALL_POINTS)

        return PointsInResponse(
            count=len(points), results=[PointInDB(**point) for point in points]
        )

    async def get_all_points_ids(
        self, user_id: Optional[int] = None
    ) -> PointsInResponse:
        if user_id:
            points_ids = await self._conn.fetch(GET_ALL_USER_POINTS, user_id)
        else:
            points_ids = await self._conn.fetch(GET_ALL_POINTS)

        return PointsInResponse(
            count=len(points_ids),
            results=[PointIDOnly(**points_id) for points_id in points_ids],
        )

    async def get_point_by_id(self, *, id: int) -> PointInDB:
        point = await self._conn.fetchrow(GET_POINT_QUERY_BY_ID, id)

        if point:
            return PointInDB(**point)

        raise EntityDoesNotExistError(f"Entity with id <{id}> does not exist")
    
    async def delete_point_by_id(self, *, id: int) -> None:
        point = await self._conn.execute(DELETE_POINT_QUERY_BY_ID, id)
