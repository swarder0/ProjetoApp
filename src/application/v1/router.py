from fastapi import APIRouter

from application.v1.endpoinits import client

router = APIRouter(prefix="/v1")
router.include_router(client.router)