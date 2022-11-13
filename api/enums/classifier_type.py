from enum import Enum


class ClassifierType(str, Enum):
    SGDClassifier = "SGDClassifier"
    CategoricalNB = "CategoricalNB"
    MLPClassifier = "MLPClassifier"
