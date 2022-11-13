from typing import List, Optional

from pydantic import BaseModel

from enums.response_type import ResponseType


class Response(BaseModel):
    status: ResponseType
    message: Optional[str]


class ModelGroup(BaseModel):
    n_trained: int
    model_ids: List[int] = None
