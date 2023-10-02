from typing import Optional

from pydantic import BaseModel
from fastapi import Depends
from fastapi import Query


class CameraData(BaseModel):
    uuid: str
    num_camera: Optional[int] = 0


def dependency_device(
        uuid: str = Query(...),
        num_camera: int = Query(...),
):
    return CameraData(
        uuid=uuid,
        num_camera=num_camera
    )


class Offer(BaseModel):
    sdp: str
    type: str
