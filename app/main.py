from fastapi import FastAPI

from app.api.routes.api import router as api_router
from app.core.config import settings



def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.title,
        description=settings.description,
        version=settings.version,
        debug=settings.debug
    )
    
    application.include_router(api_router, prefix=settings.API_PREFIX)
    
    return application

app = get_application()
