from api.utils.general_response import ErrorModel


class RequestException(Exception):
    @property
    def code(self) -> int:
        raise NotImplementedError

    @property
    def title(self) -> str:
        raise NotImplementedError

    @property
    def detail(self) -> str:
        raise NotImplementedError

    def to_pydantic(self) -> ErrorModel:
        return ErrorModel(code=self.code, title=self.title, detail=self.detail)


class Base409(RequestException):
    code = 409

    @property
    def title(self) -> str:
        raise NotImplementedError

    @property
    def detail(self) -> str:
        raise NotImplementedError
