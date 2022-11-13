from flask import Flask, g

from datasource.db import connect
from datasource.schema import DATABASE_QUERY, TABLES_QUERY
from controller.healthcheck import health_api
from controller.models import models_api

application = Flask(__name__)


def create_app():
    with application.app_context():
        setup_db()
    return application


def register_blueprints():
    application.register_blueprint(health_api, url_prefix='/health')
    application.register_blueprint(models_api, url_prefix='/models')
    return application


def get_db():
    if 'db' not in g:
        g.db = connect()
    return g.db


def setup_db():
    try:
        mysql_db = get_db()
        db_cursor = mysql_db.cursor()
        db_cursor.execute(DATABASE_QUERY)
        db_cursor.execute(TABLES_QUERY)
        db_cursor.close()
        print("Successfully instantiated DB & Tables")
    except Exception as e:
        print("Error during instantiated DB & Tables: {}".format(e))
        raise e


if __name__ == "__main__":
    create_app()
    register_blueprints()
    application.run("0.0.0.0")


@application.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()
