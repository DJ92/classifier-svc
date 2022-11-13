from enum import Enum


class ResponseType(str, Enum):
    OK = "ok"
    ERROR = "error"
