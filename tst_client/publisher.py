import asyncio
import sys
from logging import getLogger
from typing import Any, Dict, List, Optional, Union

import aiohttp
from aiortc import (
    RTCConfiguration,
    RTCIceServer,
    RTCPeerConnection,
    RTCSessionDescription,
)
from aiortc.contrib.media import MediaPlayer, MediaStreamTrack
from pydantic import BaseModel

if sys.platform != "win32":
    try:
        import uvloop

        uvloop.install()

    except ModuleNotFoundError:
        print("not installed `uvloop`")

LOGGER = getLogger("test streaming")
BASE_HOST = "http://localhost:8000"
BASE_ROUTE = "/api/stream/v1/webrtc"

UUID = "1234567890abcdef"
NUM_CAMERA = 0
PARAMS_REQUEST = dict(uuid=UUID, num_camera=NUM_CAMERA)

GET_OFFER = "/get_offer"
SEND_ANSWER = "/publisher_answer"
UNREGISTER_PUBLISHER = "/unregister_publisher"

# full path to camera with auth in rtsp protocol
PATH_IP_CAMERA = None
# PATH_IP_CAMERA = "rtsp://VehicleCamera:VehCam123!@192.168.50.252:554/stream2"


class StunTurnConfig(BaseModel):
    urls: str
    credential: Optional[str] = None
    username: Optional[str] = None


sturn_turn_config: List[StunTurnConfig] = [
    StunTurnConfig(
        urls="turn:65.108.247.69:3478",
        credential="ywmX5RdmWHth35WKUcht7FQbpTWqXS5J",
        username="drone_system",
    ),
    StunTurnConfig(urls="stun:stun.l.google.com:19302"),
]


async def make_request(
    url: str, method: str, json: Dict = None, params: Dict = None, headers: Dict = None
) -> Union[aiohttp.ClientResponse, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method, url, json=json, params=params, headers=headers
        ) as response:
            return response, await response.json()


def generate_url():
    pass


def get_media_player():
    if PATH_IP_CAMERA is None:
        if sys.platform == "win32":
            params = {
                "file": "video=Integrated Camera",
                "format": "dshow",
                "options": {"video_size": "640x480"},
                "timeout": 0.1,
            }
        elif sys.platform == "darwin":
            params = {
                "file": "default:none",
                "format": "avfoundation",
                "options": {
                    "video_size": "640x480",
                    "framerate": "30",
                },
                "timeout": 0.1,
            }
        else:
            params = {
                "file": "/dev/video0",
                "format": "v4l2",
                "options": {"video_size": "640x480"},
                "timeout": 0.1,
            }
    else:
        print("IP")
        params = {
            "file": PATH_IP_CAMERA,
            "format": "rtsp",
        }
    mp = MediaPlayer(**params)
    return mp


def get_url(postfix: str) -> str:
    return f"{BASE_HOST}{BASE_ROUTE}{postfix}"


async def start_streaming():

    # response, data = await make_request(
    #     method="DELETE",
    #     url=get_url(UNREGISTER_PUBLISHER),
    #     params=PARAMS_REQUEST,
    # )
    # print(data)

    response, data = await make_request(
        method="GET",
        url=get_url(GET_OFFER),
        params=PARAMS_REQUEST,
    )
    sdp_server = data["data"]

    offer = RTCSessionDescription(sdp=sdp_server["sdp"], type=sdp_server["type"])
    peer_connection = RTCPeerConnection(
        configuration=RTCConfiguration(
            iceServers=[
                RTCIceServer(**url_data.model_dump()) for url_data in sturn_turn_config
            ]
        )
    )
    media_player = get_media_player()
    peer_connection.addTrack(media_player.video)
    # peer_connection.addTrack(media_player.audio)

    @peer_connection.on("connectionstatechange")
    async def on_connectionstatechange():
        if (
            peer_connection.connectionState == "failed"
            or peer_connection.connectionState == "closed"
        ):
            print("close")
            await peer_connection.close()
        else:
            print(peer_connection.connectionState, peer_connection.iceConnectionState)

    await peer_connection.setRemoteDescription(offer)
    answer = await peer_connection.createAnswer()
    await peer_connection.setLocalDescription(answer)
    descr = peer_connection.localDescription

    response, data_response = await make_request(
        url=get_url(postfix=SEND_ANSWER),
        params=PARAMS_REQUEST,
        json={
            "sdp": descr.sdp,
            "type": descr.type,
        },
        method="post",
    )
    print(data_response)


async def main():
    print("main")
    await start_streaming()
    while True:
        print("alive")
        await asyncio.sleep(10)


if __name__ == "__main__":
    if sys.platform != "win32":
        try:
            import uvloop

            uvloop.install()
            LOGGER.info("Server run with uvloop")

        except ModuleNotFoundError:
            LOGGER.info("Server run without uvloop. Because uvloop not installed")

    try:
        asyncio.run(main=main())

    except KeyboardInterrupt:
        LOGGER.info("Server is stopped.")
