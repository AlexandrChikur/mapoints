import math
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from app.models.common import IDModelMixin


class Point(BaseModel):
    name: Optional[str] = Field(None, max_length=24)
    x: int
    y: int

    def get_distance_to_another_point(self, point) -> float:
        return math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)


class PointInDB(Point, IDModelMixin):
    user_id: int


class PointInCreate(Point):
    user_id: int


class PointIDOnly(IDModelMixin):
    pass


class PointsInResponse(BaseModel):
    count: int
    results: List[Union[PointInDB, PointIDOnly]]
