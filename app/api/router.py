from fastapi import APIRouter
from app.api.task import task_router
from app.api.user import user_router

router = APIRouter()
router.include_router(router=task_router, prefix="/tasks", tags=["tasks"])
router.include_router(router=user_router, prefix="/users", tags=["users"])
