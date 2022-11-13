from flask import Blueprint

from enums.response_type import ResponseType
from entities.response import Response

health_api = Blueprint('health', __name__)


@health_api.route("/", methods=['GET'])
def health():
    return Response(status=ResponseType.OK).json()

