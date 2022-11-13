import base64
import json

import numpy as np
import pickle

from flask import jsonify, Blueprint
from flask_pydantic import validate

from entities.request import ClassifierModel, TrainModel
from entities.response import Response
from enums.classifier_type import ClassifierType
from enums.response_type import ResponseType

from datasource.db import connect
from datasource.schema import GET_ALL_MODELS, GET_ALL_TRAINED_MODELS, \
    GET_MODEL_QUERY, INSERT_MODEL_QUERY, INSERT_MODEL_TRAINING_QUERY, UPDATE_MODEL_QUERY

from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import CategoricalNB
from sklearn.neural_network import MLPClassifier


models_api = Blueprint('models', __name__)


@models_api.route("/", methods=["POST"])
@validate()
def create_model(body: ClassifierModel):
    if body.model == ClassifierType.SGDClassifier:
        model_obj = SGDClassifier(**body.params)
    elif body.model == ClassifierType.CategoricalNB:
        model_obj = CategoricalNB(**body.params)
    else:
        model_obj = MLPClassifier(**body.params)
    model_data = pickle.dumps(model_obj)
    model_params = json.dumps(body.params)
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(INSERT_MODEL_QUERY, (body.model, body.d, body.n_classes, 0, model_params, model_data))
        model_id = cur.lastrowid
        if model_id > 0:
            cur.close()
            conn.commit()
            conn.close()
        return jsonify({"id": model_id})
    except Exception as e:
        return Response(status=ResponseType.ERROR, message="Error during creating model: {}".format(e)).json()


@models_api.route("/<model_id>/", methods=["GET"])
def get_model(model_id: int):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(GET_MODEL_QUERY, (model_id,))
        row = cur.fetchone()
        if row:
            model = ClassifierModel(
                model=row[1], d=row[2], n_classes=row[3], n_trained=row[4], params=json.loads(row[5])
            )
            cur.close()
            conn.commit()
            conn.close()
            return model.json()
        else:
            return Response(status=ResponseType.ERROR, message="Error during fetching model: {}".format(row)).json()
    except Exception as e:
        return Response(status=ResponseType.ERROR, message="Error during fetching model: {}".format(e)).json()


@models_api.route("/<model_id>/train/", methods=["POST"])
@validate()
def train_model(model_id: int, body: TrainModel):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(GET_MODEL_QUERY, (model_id,))
        row = cur.fetchone()
        if row:
            model_id = row[0]
            d = int(row[2])
            n_classes = int(row[3])
            n_trained = int(row[4])
            model_data = row[6]
            model_obj = pickle.loads(model_data)
            model_obj.partial_fit(X=[np.array(body.x)], y=[body.y], classes=np.arange(0, n_classes, 1))
            cur.execute(INSERT_MODEL_TRAINING_QUERY, (model_id,))
            model_data = pickle.dumps(model_obj)
            cur.execute(UPDATE_MODEL_QUERY, (n_trained+1, model_data, model_id))
            if cur.rowcount:
                cur.close()
                conn.commit()
                conn.close()
            return Response(status=ResponseType.OK).json()
        else:
            return Response(status=ResponseType.ERROR, message="Error during training model: {}".format(row)).json()
    except Exception as e:
        return Response(status=ResponseType.ERROR, message="Error during training model: {}".format(e)).json()


@models_api.route("/<model_id>/predict/<x>", methods=["GET"])
def predict_model(model_id: int, x: str = None):
    try:
        x_str = base64.b64decode(x).decode("utf-8").replace('[', '').replace(']', '')
        x_arr = [float(x) for x in x_str.split(",")]
        conn = connect()
        cur = conn.cursor()
        cur.execute(GET_MODEL_QUERY, (model_id,))
        row = cur.fetchone()
        if row:
            model_data = row[6]
            model_obj = pickle.loads(model_data)
            result = model_obj.predict([x_arr])[0]
            cur.close()
            conn.close()
            return jsonify({"x": x_arr, "y": result.item()})
        else:
            return Response(status=ResponseType.ERROR, message="Error during model prediction: {}".format(row)).json()
    except Exception as e:
        return Response(status=ResponseType.ERROR, message="Error during model prediction: {}".format(e)).json()


@models_api.route("/", methods=["GET"])
def get_models():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(GET_ALL_MODELS)
        rows = cur.fetchall()
        model_list = []
        model_map = {}
        for model_id, model_name, _, _, n_trained, _, _ in rows:
            if model_map.get(model_name) is None:
                model_map[model_name] = [n_trained]
            else:
                value = model_map[model_name]
                value.append(n_trained)
                model_map[model_name] = value
            model_list.append({
                "id": model_id,
                "model": model_name,
                "n_trained": n_trained,
                "training_score": 0.0
            })

        for model in model_list:
            trained_values = model_map[model["model"]]
            x = model["n_trained"]
            if (max(trained_values) - min(trained_values)) == 0:
                training_score = 1.0
            else:
                training_score = (x - min(trained_values)) / (max(trained_values) - min(trained_values))
            model["training_score"] = training_score

        models = {"models": model_list}
        cur.close()
        conn.close()
        return jsonify(models)
    except Exception as e:
        return Response(status=ResponseType.ERROR, message="Error during fetching model groups: {}".format(e)).json()


@models_api.route("/groups/", methods=["GET"])
def get_model_groups():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(GET_ALL_TRAINED_MODELS)
        rows = cur.fetchall()
        group_list = []
        for num_trained, models in rows:
            group_list.append({"n_trained": num_trained, "model_ids": [int(id) for id in models.split(",")]})
        groups = {"groups": group_list}
        cur.close()
        conn.close()
        return jsonify(groups)
    except Exception as e:
        return Response(status=ResponseType.ERROR, message="Error during fetching model groups: {}".format(e)).json()
