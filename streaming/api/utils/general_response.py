from typing import Any, Dict, Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

SubPydanticBaseModel = TypeVar("SubPydanticBaseModel", bound=BaseModel)


class ErrorModel(BaseModel):
    code: int = Field(default=400, description="http status code")
    title: str = Field(description="Error group")
    detail: str = Field(description="Details error")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 400,
                "title": "IncorrectInputData",
                "detail": "Type of `sku_id` must be a integer and not a string",
            }
        }


class SuccessExecutionWithoutResponseData(BaseModel):
    msg: str = Field("success")

    class Config:
        json_schema_extra = {
            "example": {
                "msg": "success",
            }
        }


class BadResponse(BaseModel):
    status: str = "error"
    error: ErrorModel


class RespModel(GenericModel, Generic[SubPydanticBaseModel]):
    status: str
    data: SubPydanticBaseModel


def get_response(
        data: BaseModel,
        headers: Optional[Dict[str, Any]] = None,
        status_code: int = 200,
        cookies: Optional[Dict[str, str]] = None,
) -> JSONResponse:
    if isinstance(data, ErrorModel):
        content = dict(status="error", data=jsonable_encoder(data))
        status_code = data.code
    else:
        content = dict(status="success", data=jsonable_encoder(data))
    response = JSONResponse(content=content, headers=headers, status_code=status_code)
    if cookies:
        for cookie_name, cookie_value in cookies.items():
            response.set_cookie(key=cookie_name, value=cookie_value)
    return response
