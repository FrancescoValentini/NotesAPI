from fastapi import APIRouter

from api.v1.endpoints import auth, notes

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(notes.router)