from fastapi import APIRouter

from app.api.routes import maps, points

router = APIRouter()

router.include_router(maps.router, tags=["maps"], prefix="/maps")
router.include_router(points.router, tags=["points"], prefix="/points")