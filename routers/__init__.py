from fastapi import APIRouter

from routers.auth import auth_router
from routers.trip import trip_agents


router = APIRouter()
router.include_router(auth_router)
router.include_router(trip_agents)

