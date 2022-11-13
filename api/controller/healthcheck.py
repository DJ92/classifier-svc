from flask import Blueprint

from controller.entities.response import Response
from enums.response_type import ResponseType

health_api = Blueprint('health', __name__)


@health_api.route("", methods=['GET'])
def health():
    return Response(status=ResponseType.OK).json()

