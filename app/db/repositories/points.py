from typing import Optional
from asyncpg.exceptions import CheckViolationError

from app.core.config import settings
from app.db.errors.common import EntityDoesNotExistError, PointsCapacityReachedMaxValueError
from app.db.queries.points import *
from app.models.schemas.points import PointIDOnly, PointInDB, PointsInResponse, PointFullData

from .base import BaseRepository


class PointsRepository(BaseRepository):
    async def create_point(
        self, *, name: str, x: int, y: int, user_id: int
    ) -> PointInDB:
        point = PointInDB(name=name, x=x, y=y, user_id=user_id)
        try:
            await self._conn.execute(CREATE_POINT_INCREMENT_QUERY, user_id)
        except CheckViolationError:
            raise PointsCapacityReachedMaxValueError(f"The number of points has reached its maximum value ({settings.DEFAULT_POINTS_CAPACITY}) for user with id: <{user_id}>")
        
        id_record = await self._conn.fetchrow(
            CREATE_POINT_QUERY_RETURNING_ID, point.name, point.x, point.y, user_id
        )
        id = id_record.get("id", None) 
        point.id = id

        return point

    async def get_all_points(self, user_id: Optional[int] = None, lookup: Optional[str] = None) -> PointsInResponse:
        if user_id:
            points = await self._conn.fetch(GET_ALL_USER_POINTS, user_id)
        else:
            if lookup:
                points = await self._conn.fetch(GET_ALL_POINTS_LOOKUP, f"%{lookup}%")
            else:
                points = await self._conn.fetch(GET_ALL_POINTS)
        return PointsInResponse(
            count=len(points), results=[PointFullData(**point) for point in points]
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

    async def get_point_by_id(self, *, id: int) -> PointFullData:
        point = await self._conn.fetchrow(GET_POINT_QUERY_BY_ID, id)
        if point:
            return PointFullData(**point)

        raise EntityDoesNotExistError(f"Entity with id <{id}> does not exist")
    
    async def delete_point_by_id(self, *, id: int, owner_id: int) -> None:
        await self._conn.execute(DELETE_POINT_QUERY_BY_ID, id)
        await self._conn.execute(CREATE_POINT_DECREMENT_QUERY, owner_id)