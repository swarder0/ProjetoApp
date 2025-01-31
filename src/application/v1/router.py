from fastapi import APIRouter

from src.application.v1.endpoints import client

router = APIRouter(prefix="/v1")
router.include_router(client.router)