import logging

from flask import Flask

from datasource.db import connect
from datasource.schema import DATABASE_QUERY, TABLES_QUERY
from controller.healthcheck import health_api
from controller.models import models_api

application = Flask(__name__)
logger = logging.getLogger(__name__)

application.register_blueprint(health_api, url_prefix='/health')
application.register_blueprint(models_api, url_prefix='/models')


@application.before_first_request
def setup_db():
    try:
        logger.info("Initializing DB")
        mysql_db = connect()
        db_cursor = mysql_db.cursor()
        logger.info("Setting up schema")
        db_cursor.execute(DATABASE_QUERY)
        db_cursor.execute(TABLES_QUERY)
        db_cursor.close()
        mysql_db.commit()
        mysql_db.close()
        logger.info("Successfully instantiated DB & Tables")
    except Exception as e:
        logger.error("Error during instantiated DB & Tables: {}".format(e))
        raise e


if __name__ == "__main__":
    application.run("0.0.0.0")

