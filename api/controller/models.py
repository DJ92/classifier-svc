from flask import jsonify, Blueprint
from flask_pydantic import validate

from api.controller.entities.request import ClassifierModel, TrainModel
from api.controller.entities.response import Response
from api.enum.classifier_type import ClassifierType
from api.enum.response_type import ResponseType

models_api = Blueprint('models', __name__)


@models_api.route("", methods=["POST"])
@validate()
def create_model(body: ClassifierModel):
    return body.json()


@models_api.route("/<model_id>", methods=["GET"])
def get_model(model_id: int):
    print(model_id)
    message = {
        "model": ClassifierType.MLPClassifier,
        "params": {"alpha": 0.0001, "hidden_layer_sizes": 20},
        "d": 4,
        "n_classes": 2
    }
    return jsonify(message)


@models_api.route("/<model_id>/train", methods=["POST"])
@validate()
def train_model(model_id: int, body: TrainModel):
    print(model_id)
    return body.json()


@models_api.route("/<model_id>/predict/<x>", methods=["GET"])
def predict_model(model_id: int, x: str = None):
    print(model_id)
    print(x)
    message = {
        "x": [1.11, 2.22, 3.33, -4.44],
        "y": 1
    }
    return jsonify(message)


@models_api.route("/groups", methods=["GET"])
def get_model_groups():
    message = {
        "groups": [
            {
                 "n_trained": 4,
                 "model_ids": [1, 129]
            },
            {
                    "n_trained": 2198423,
                    "model_ids": [13, 121, 17]
            }
        ]
    }
    return jsonify(message)
