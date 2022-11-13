"""
TODO. For instance:

1. using flask:

from flask import Flask
application = Flask(__name__)


2. using django:

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your.django.settings")
application = get_wsgi_application()


3. using raw WSGI (https://www.python.org/dev/peps/pep-3333/#the-application-framework-side):

def application(environ, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])
    return ['{"message": "ok"}']
"""

from flask import Flask

from datasource.schema import DATABASE_QUERY, TABLES_QUERY
from db import connect

application = Flask(__name__)
mysql_db = connect()


def setup_db():
    db_cursor = mysql_db.connection.cursor()
    db_cursor.execute(DATABASE_QUERY)
    db_cursor.execute(TABLES_QUERY)


if __name__ == "__main__":
    setup_db()
    application.run(host='0.0.0.0')
