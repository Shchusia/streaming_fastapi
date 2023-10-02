from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.utils.general_response import get_response
from .exc import RequestException
from .settings import CoreSettings
from starlette.middleware.cors import CORSMiddleware
from .session_storage import setup_session_storage
from api.v1.v1_router import api_router
from utils.logger_middleware import LoggingMiddleware
from starlette_prometheus import PrometheusMiddleware, metrics

def init_app():
    CONFIG = CoreSettings()
    APP = FastAPI(
        title=CONFIG.title_app,
        description=CONFIG.description_app,
        openapi_url=f"{CONFIG.base_url}"
                    f"{CONFIG.global_url_prefix}/"
                    f"{CONFIG.api_version}/openapi.json",
        debug=CONFIG.is_debug,
        docs_url=f"{CONFIG.base_url}/docs",
    )
    APP.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        # allow_methods=["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"],
        allow_methods=["*"],
        allow_headers=["*"],
        # allow_headers='date,server,content-length,content-type,access-control-allow-credentials,access-control-allow-origin,vary,Content-Type,Authorization,X-Requested-With,at,rt,AT,RT'.split(
        #     ','),
        expose_headers=["*"]
        # expose_headers='date, server, content-length, content-type, access-control-allow-credentials, access-control-allow-origin, vary'.split(
        #     ', ')
    )
    setup_session_storage()

    APP.middleware("http")(LoggingMiddleware())
    APP.add_middleware(PrometheusMiddleware)

    APP.include_router(api_router, prefix=f"{CONFIG.base_url}{CONFIG.global_url_prefix}")
    APP.add_route(f"{CONFIG.base_url}/metrics", metrics)

    @APP.exception_handler(RequestException)
    def custom_exception_handler(request: Request, exc: RequestException) -> JSONResponse:
        return get_response(data=exc.to_pydantic())

    return APP
