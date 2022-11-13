from typing import List

from pydantic import BaseModel

from api.enums.response_type import ResponseType


class Response(BaseModel):
    status: ResponseType


class ModelGroup(BaseModel):
    n_trained: int
    model_ids: List[int] = None
