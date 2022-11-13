# Classifier Service

## API Spec

1. GET /health - ok [200]
<br>Response
```json
{
    "status": "ok",
    "message": null
}
```

2. POST /models - [200/400/404/405]
<br>Request
```json
{
    "model": "MLPClassifier",
    "params": {
        "alpha": 0.0001,
        "hidden_layer_sizes": 20
    },
    "d": 4,
    "n_classes": 2
} 
```
<br>Response
```json
{
    "id": 4
}
```

3. GET /models/<model_id> - [200/400/404/405]
<br>Response
```json
{
    "model": "MLPClassifier",
    "params": {
        "alpha": 0.0001,
        "hidden_layer_sizes": 20
    },
    "d": 4,
    "n_classes": 2,
    "n_trained": 48
}
```

4. POST /models/<model_id>/train - [200/400/404/405]
<br>Request
```json
{
    "x": [
        1.11,
        2.22,
        3.33,
        4.44
    ],
    "y": 1
}
```
<br>Response
```json
{
    "status": "ok",
    "message": null
}
```

5. GET - /models/<model_id>/predict/<x> - [200/400/404/405]
<br>Response
```json
{
    "x": [
        1.11,
        2.22,
        3.33,
        -4.44
    ],
    "y": 0
}
```

6. GET - /models/ - [200/400/404/405]
<br>Response
```json
{
    "models": [
        {
            "id": 1,
            "model": "MLPClassifier",
            "n_trained": 4,
            "training_score": 0.0
        },
        {
            "id": 2,
            "model": "CategoricalNB",
            "n_trained": 4,
            "training_score": 1.0
        },
        {
            "id": 3,
            "model": "MLPClassifier",
            "n_trained": 13,
            "training_score": 0.20454545454545456
        },
        {
            "id": 4,
            "model": "MLPClassifier",
            "n_trained": 48,
            "training_score": 1.0
        }
    ]
}
```

7. GET - /models/groups/ - [200/400/404/405]
<br>Response
```json
{
    "groups": [
        {
            "model_ids": [
                1,
                2
            ],
            "n_trained": 4
        },
        {
            "model_ids": [
                3
            ],
            "n_trained": 13
        },
        {
            "model_ids": [
                4
            ],
            "n_trained": 48
        }
    ]
}
```

## DB Schema

Model
```sql
CREATE TABLE IF NOT EXISTS MODEL(
    ModelId INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(20) NOT NULL,
    NumFeatures INT NOT NULL,
    NumClasses INT NOT NULL,
    NumTrained INT NOT NULL,
    ModelParams VARCHAR(200) NOT NULL,
    ModelData BLOB NOT NULL,
    PRIMARY KEY (ModelId)
);
```

ModelTraining
```sql
CREATE TABLE IF NOT EXISTS MODEL_TRAINING(
    TrainingId INT NOT NULL AUTO_INCREMENT,
    ModelId INT NOT NULL,
    FOREIGN KEY (ModelId) REFERENCES MODEL(ModelId),
    PRIMARY KEY (TrainingId)
);
```

## Tests / QA

Postman: https://www.getpostman.com/collections/30872a4bf7a3c0b7c25d
