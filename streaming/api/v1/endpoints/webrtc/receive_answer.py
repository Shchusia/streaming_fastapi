from typing import Annotated

from aiortc import RTCSessionDescription
from api.utils.general_response import SuccessExecutionWithoutResponseData, get_response
from core.session_storage import EnumAppKeys, SessionStorage
from fastapi import Body, Depends, Query

from ...exc import NotGeneratedPeerConnectionForVehicle
from ...schemas.webrtc import CameraData, Offer, dependency_device
from .router import webrtc_router
from .routes import WebrtcRoutes


@webrtc_router.post(
    path=WebrtcRoutes.POST_RECEIVE_ANSWER,
)
async def receive_answer_route(
    storage: Annotated[SessionStorage, Depends(SessionStorage())],
    payload: Annotated[CameraData, Depends(dependency_device)],
    offer: Offer = Body(...),
):
    if storage[EnumAppKeys.STREAM_CONNECTIONS].get(payload.uuid, None) is None:
        return NotGeneratedPeerConnectionForVehicle.get_response(
            uuid=payload.uuid, num_camera=payload.num_camera
        )
    if (
        peer_connection := storage[EnumAppKeys.STREAM_CONNECTIONS][payload.uuid].get(
            payload.num_camera, None
        )
    ) is None:
        return NotGeneratedPeerConnectionForVehicle.get_response(
            uuid=payload.uuid, num_camera=payload.num_camera
        )

    await peer_connection.setRemoteDescription(
        sessionDescription=RTCSessionDescription(
            sdp=offer.sdp,
            type=offer.type,
        )
    )
    return get_response(SuccessExecutionWithoutResponseData())
