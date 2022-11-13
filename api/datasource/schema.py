DATABASE_QUERY = '''
    CREATE DATABASE IF NOT EXISTS CHALLENGE; 
    USE CHALLENGE;
'''

TABLES_QUERY = '''
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
    
    CREATE TABLE IF NOT EXISTS MODEL_TRAINING(
        TrainingId INT NOT NULL AUTO_INCREMENT,
        ModelId INT NOT NULL,
        FOREIGN KEY (ModelId) REFERENCES MODEL(ModelId),
        PRIMARY KEY (TrainingId)
    );
'''

INSERT_MODEL_QUERY = '''
    INSERT INTO MODEL(Name, NumFeatures, NumClasses, NumTrained, ModelParams, ModelData)
    VALUES (%s, %s, %s, %s, %s, %s);
'''

INSERT_MODEL_TRAINING_QUERY = '''
    INSERT INTO MODEL_TRAINING(ModelId)
    VALUES (%s);
'''

GET_MODEL_QUERY = '''
    SELECT * FROM MODEL WHERE ModelId = %s;
'''

UPDATE_MODEL_QUERY = '''
    UPDATE MODEL
    SET NumTrained = %s, ModelData = %s
    WHERE ModelId = %s;
'''

GET_ALL_TRAINED_MODELS = '''
    SELECT NumTrained, GROUP_CONCAT(DISTINCT ModelId) FROM MODEL
    GROUP BY NumTrained;
'''

GET_ALL_MODELS = '''
    SELECT * FROM MODEL;
'''