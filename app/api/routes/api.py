from fastapi import APIRouter

from app.api.routes import maps, points, users

router = APIRouter()

router.include_router(maps.router, tags=["maps"], prefix="/maps")
router.include_router(points.router, tags=["points"], prefix="/points")
router.include_router(users.router, tags=["users"], prefix="/users")
