from fastapi import HTTPException, status

from app.core.config import settings
from app.resources.strings import *


class PointsCapacityReachedError(HTTPException):
    """Raised when the max points capacity for specific user reached """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail=MAX_POINT_CAPACITY_REACHED.format(settings.DEFAULT_POINTS_CAPACITY)
        )