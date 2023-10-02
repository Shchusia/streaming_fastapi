from pydantic_settings import BaseSettings
from pydantic import Field, BaseModel
from typing import Optional, List
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_SRC = BASE_DIR / "src"
class CoreSettings(BaseSettings):
    # #######################
    # ### config main APP ###
    # #######################
    title_app: str = Field("Stream data", description="Title application")
    description_app: str = Field(
        "Api for streaming", description="Description this app"
    )
    is_debug: bool = Field(False, description="Run on debug mode")
    # ###################
    # ### urls config ###
    # ###################
    base_url: str = Field("/api", description="Base URL of all routes application")
    global_url_prefix: str = Field(
        "/stream",
        description="Global prefix for build url. "
                    "Build url base_url + global_url_prefix "
                    "+ api_version_prefix + api_prefix",
    )
    api_version: str = Field("0.0.1", description="Current API Version")
    prometheus_metrics_url: str = Field(
        "/metrics", description="Url to prometheus metrics."
    )


class StunTurnConfig(BaseModel):
    urls: str
    credential: str | None = None
    username: str | None = None


class StreamSettings(BaseSettings):
    save_video: bool = Field(True, description="Save streamed video")
    sturn_turn_config: List[StunTurnConfig] = [
        StunTurnConfig(
            urls="turn:65.108.247.69:3478",
            credential="ywmX5RdmWHth35WKUcht7FQbpTWqXS5J",
            username="drone_system",
        ),
        StunTurnConfig(urls="stun:stun.l.google.com:19302"),
    ]


DATE_FORMAT_SAVE_FILE = "%Y-%m-%d__%H:%M:%S"
