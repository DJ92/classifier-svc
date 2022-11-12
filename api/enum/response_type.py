from enum import Enum


class ResponseType(str, Enum):
    OK = "Ok"
    ERROR = "Error"
