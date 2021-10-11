from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Point(BaseModel):
    uid: UUID
    name: Optional[str] = None
    x: int
    y: int