from uuid import uuid4

from app.db.queries.points import *
from app.models.schemas.points import Point, PointInDB, PointsInResponse

from .base import BaseRepository


class PointsRepository(BaseRepository):
    async def create_point(self, *, name: str, x: int, y: int) -> PointInDB:
        uid = uuid4()
        point = PointInDB(uid=uid, name=name, x=x, y=y)
        await self._conn.execute(
            CREATE_POINT_QUERY, point.uid, point.name, point.x, point.y
        )

        return point

    async def get_all_points(self) -> PointsInResponse:
        points = await self._conn.fetch(GET_ALL_POINTS)

        return PointsInResponse(
            count=len(points), results=[PointInDB(**point) for point in points]
        )

    async def get_point_by_uid(self):
        pass
