import logging
from pathlib import Path

from core.settings import MEDIA_SRC,DATE_FORMAT_SAVE_FILE
from datetime import date, datetime
from aiortc import MediaStreamTrack, RTCConfiguration, RTCIceServer, RTCPeerConnection
from aiortc.mediastreams import MediaStreamError
from asgiref.sync import async_to_sync, sync_to_async

import av
LOGGER = logging.getLogger()

async def get_path_to_folder(uuid: str):
    path_to_folder = MEDIA_SRC
    path_to_folder /= Path(uuid)
    path_to_folder /= date.today().isoformat()
    path_to_folder.mkdir(parents=True, exist_ok=True)
    return path_to_folder

def sync_save(frame, out_stream, file):
    for packet in out_stream.encode(frame):
        file.mux(packet)

async def save_video(track: MediaStreamTrack, uuid: str, num_camera: int):
    """
    method for saving video from device
    :param track: remote media stream track
    :param uuid: uuid of the device
    :param num_camera: on device
    :return: nothing
    """
    path = await get_path_to_folder(uuid)
    file_name = (
        f"{uuid}_cam_{num_camera}__{datetime.now().strftime(DATE_FORMAT_SAVE_FILE)}.mp4"
    )
    with av.open(str(path / file_name), "w") as file:
        out_stream = file.add_stream("h264", rate=30)
        is_added_size = False

        while True:
            try:
                frame = await track.recv()
                if not is_added_size:
                    out_stream.width = (
                        frame.width
                    )  # Set frame width to be the same as the width of the input stream
                    out_stream.height = frame.height
                    is_added_size = True
                await sync_to_async(sync_save)(frame, out_stream, file)
            except MediaStreamError:
                print("\n\nError decoding")
                break
            except Exception as exc:
                LOGGER.warning("error saving video. %s", str(exc), exc_info=True)
                break
        for packet in out_stream.encode():
            file.mux(packet)
