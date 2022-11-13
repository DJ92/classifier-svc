"""
TODO. For instance:

1. using flask:

from flask import Flask
application = Flask(__name__)


2. using django:

from django.core.wsgi.py import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your.django.settings")
application = get_wsgi_application()


3. using raw WSGI (https://www.python.org/dev/peps/pep-3333/#the-application-framework-side):

def application(environ, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])
    return ['{"message": "ok"}']
"""
from flask import Flask

from datasource.db import connect
from datasource.schema import DATABASE_QUERY, TABLES_QUERY
from controller.healthcheck import health_api
from controller.models import models_api

application = Flask(__name__)

application.register_blueprint(health_api, url_prefix='/health')
application.register_blueprint(models_api, url_prefix='/models')

mysqldb = None


def setup_db():
    try:
        mysql_db = connect()
        db_cursor = mysql_db.cursor()
        db_cursor.execute(DATABASE_QUERY)
        db_cursor.execute(TABLES_QUERY)
        db_cursor.close()
        print("Successfully instantiated DB & Tables")
    except Exception as e:
        print("Error during instantiated DB & Tables: {}".format(e))
        raise e


if __name__ == "__main__":
    setup_db()
    application.run(host='0.0.0.0')
