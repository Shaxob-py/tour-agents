from fastapi import APIRouter

from routers.ai import ai_router
from routers.auth import auth_router
# from routers.users import user_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(ai_router)
# router.include_router(user_router)