from typing import Annotated

from aiortc import RTCSessionDescription
from api.utils.general_response import SuccessExecutionWithoutResponseData, get_response
from core.session_storage import EnumAppKeys, SessionStorage
from fastapi import Body, Depends, Query

from ...schemas.webrtc import CameraData, Offer, dependency_device
from .router import webrtc_router
from .routes import WebrtcRoutes


@webrtc_router.delete(
    path=WebrtcRoutes.DELETE_UNREGISTER_PUBLISHER,
)
async def unregister_publisher_route(
    storage: Annotated[SessionStorage, Depends(SessionStorage())],
    payload: Annotated[CameraData, Depends(dependency_device)],
):
    try:
        await storage[EnumAppKeys.STREAM_CONNECTIONS][payload.uuid][
            payload.num_camera
        ].close()
        storage[EnumAppKeys.STREAM_CONNECTIONS][payload.uuid][payload.num_camera] = None
    except Exception:
        pass
    try:
        del storage[EnumAppKeys.STREAM_RECORDS][payload.uuid][payload.num_camera]
    except Exception:
        pass
    return get_response(SuccessExecutionWithoutResponseData())
