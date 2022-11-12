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

from api.controller.healthcheck import health_api
from api.controller.models import models_api

application = Flask(__name__)

application.register_blueprint(health_api, url_prefix='/health')
application.register_blueprint(models_api, url_prefix='/models')


if __name__ == "__main__":
    application.run(host='0.0.0.0')
