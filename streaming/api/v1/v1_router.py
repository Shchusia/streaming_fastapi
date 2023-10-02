from fastapi import APIRouter
from .endpoints.webrtc import webrtc_router
from .routes import BaseRoutesEnum

api_prefix = "/v1"

api_router = APIRouter(prefix=api_prefix)

api_router.include_router(webrtc_router, prefix=BaseRoutesEnum.WEBRTC, tags=["WEBRTC"])
