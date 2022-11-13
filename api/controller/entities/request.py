from typing import Union, List, Dict

from pydantic import BaseModel

from api.enums.classifier_type import ClassifierType


class ClassifierModel(BaseModel):
    model: ClassifierType
    d: int
    n_classes: int
    params: Dict[str, Union[str, int, float, List[int], List[float]]] = {}


class TrainModel(BaseModel):
    x: List[float]
    y: int
