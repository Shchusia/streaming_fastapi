from typing import Annotated

from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaRelay
from fastapi import Depends

from api.utils.general_response import RespModel, get_response
from core.session_storage import SessionStorage, EnumAppKeys
from core.settings import StreamSettings
from utils.video_save import save_video
from .router import webrtc_router
from .routes import WebrtcRoutes
from ...schemas.webrtc import Offer, dependency_device, CameraData

CONFIG = StreamSettings()


async def init_peer_connection(
        storage: StreamSettings, num_camera: int, uuid: str
) -> RTCPeerConnection:
    peer_connection = RTCPeerConnection(
        configuration=RTCConfiguration(
            iceServers=[
                RTCIceServer(**url_data.dict()) for url_data in CONFIG.sturn_turn_config
            ]
        )
    )

    @peer_connection.on("track")
    async def on_track(track):
        setattr(track, "kind", "video")
        relay = MediaRelay()
        new_track = relay.subscribe(track)
        storage[EnumAppKeys.STREAM_RECORDS][uuid][num_camera] = new_track
        if CONFIG.save_video:
            await save_video(new_track, uuid=uuid, num_camera=num_camera)

    @peer_connection.on("negotiationneeded")
    async def on_onnegotiationneeded():
        print("negotiationneeded")

    peer_connection.addTransceiver("video")
    offer = await peer_connection.createOffer()
    await peer_connection.setLocalDescription(offer)
    storage[EnumAppKeys.STREAM_CONNECTIONS][uuid][num_camera] = peer_connection
    return peer_connection


@webrtc_router.get(
    path=WebrtcRoutes.GET_OFFER_SERVER,
    summary="Get offer",
    description="Get server offer for customer",
    response_model=RespModel[Offer],
)
async def get_server_offer_route(
        storage: Annotated[SessionStorage, Depends(SessionStorage())],
        payload: Annotated[CameraData, Depends(dependency_device)],

):
    # todo:check access

    if (
            peer_connection := storage[EnumAppKeys.STREAM_CONNECTIONS][payload.uuid].get(
                payload.num_camera, None
            )
    ) is None:
        peer_connection = await init_peer_connection(
            storage=storage, num_camera=payload.num_camera, uuid=payload.uuid
        )
    description = peer_connection.localDescription

    return get_response(Offer(
        sdp=description.sdp,
        type=description.type,
    ))
