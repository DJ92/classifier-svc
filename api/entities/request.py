from typing import List, Dict, Optional

from pydantic import BaseModel

from enums.classifier_type import ClassifierType


class ClassifierModel(BaseModel):
    model: ClassifierType
    params: Dict = {}
    d: int
    n_classes: int
    n_trained: Optional[int]


class TrainModel(BaseModel):
    x: List[float]
    y: int
