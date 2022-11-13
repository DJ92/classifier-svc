DATABASE_QUERY = '''
    CREATE DATABASE IF NOT EXISTS CHALLENGE; 
    USE CHALLENGE;
'''

TABLES_QUERY = '''
    CREATE TABLE IF NOT EXISTS MODEL(
        ModelId INT NOT NULL AUTO_INCREMENT,
        Name VARCHAR(10) NOT NULL,
        NumFeatures INT,
        NumClasses INT,
        NumTrained INT,
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
    INSERT INTO MODEL(Name,NumFeatures,NumClasses,NumTrained)
    VALUES (%s, %s, %s, %s, %s);
'''

INSERT_MODEL_TRAINING_QUERY = '''
    INSERT INTO MODEL_TRAINING(ModelId,NumFeatures)
    VALUES (%s, %s);
'''