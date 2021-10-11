from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class Point(BaseModel):
    name: Optional[str] = None
    x: int
    y: int


class PointInDB(Point):
    uid: UUID


class PointsInResponse(BaseModel):
    count: int
    results: List[PointInDB]
