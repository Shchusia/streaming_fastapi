from __future__ import annotations
from collections import defaultdict
from typing import Optional, Any, Annotated

from utils.singletone import SingletonMeta
from enum import Enum


class SessionStorage(metaclass=SingletonMeta):
    def __init__(self):
        self.__global_dict = defaultdict(dict)

    def __getitem__(self, key) -> Optional[Any]:
        return self.__global_dict.get(key, None)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__global_dict[key] = value

    def __call__(self, ) -> SessionStorage:
        return self

    def get(self, key, default=None):
        return self.__global_dict.get(key, default)


class EnumAppKeys(str, Enum):
    STREAM_CONNECTIONS = "streams"
    STREAM_RECORDS = "records"
    CONNECTIONS = "connections"


def setup_session_storage():
    storage = SessionStorage()
    storage[EnumAppKeys.STREAM_RECORDS] = defaultdict(lambda: defaultdict(dict))
    storage[EnumAppKeys.STREAM_CONNECTIONS] = defaultdict(lambda: defaultdict(dict))
    storage[EnumAppKeys.CONNECTIONS] = defaultdict(lambda: defaultdict(dict))



