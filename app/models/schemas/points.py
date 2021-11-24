import math
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class Point(BaseModel):
    name: Optional[str] = Field(None, max_length=24)
    x: int
    y: int


    def get_distance_to_another_point(self, point) -> float:
        return math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)


class PointInDB(Point):
    uid: UUID


class PointUID(BaseModel):
    uid: UUID


class PointsInResponse(BaseModel):
    count: int
    results: List[Union[PointInDB, PointUID]]
