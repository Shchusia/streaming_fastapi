"""

"""
import time
from logging import Logger, getLogger
from typing import Optional

from fastapi import Request, Response


class LoggingMiddleware:
    """ """

    def __init__(self, logger: Optional[Logger] = None):
        self.__logger = logger or getLogger(__name__)

    def __call__(self, request: Request, call_next) -> Optional[Response]:
        start = time.time()
        is_error = False
        msg: str = ""
        error: Exception
        try:
            response = call_next(request)
        except Exception as exc:
            is_error = True
            msg = str(exc)
            error = exc
        finally:
            end = time.time()
        time_executed = "{0:.5f}".format((end - start) * 1000)
        if is_error:
            self.__logger.error(
                "Backend[Error]: %s"
                "method: %s \n"
                "url: %s \n"
                "time: %s \n"
                "requestBody: %s\n",
                "requestHeaders: %s\n",
                "requestPathParams: %s\n",
                "requestQueryParams: %s\n",
                msg,
                request.method,
                request.url,
                time_executed,
                request.body(),
                request.headers,
                request.path_params,
                request.query_params,
            )
            raise error  # noqa
        else:
            self.__logger.info(
                "WishMaster[Info]: Success" "method: %s \n" "url: %s \n" "time: %s \n",
                request.method,
                request.url,
                time_executed,
            )
            print(
                f"WishMaster[Info]: Success"
                f" method: {request.method} \n"
                f"url: {request.url} \n"
                f"time: %s {time_executed}\n"
                f"body: {request.body}"
            )
            return response