from flask import Blueprint, jsonify, Response, json
from werkzeug.exceptions import HTTPException

bp = Blueprint("error_handling", __name__)


# Error handlers
@bp.app_errorhandler(HTTPException)
def handle_exception(exception) -> Response:
    response = exception.get_response()
    response.data = json.dumps({
        "error": str(exception.code) + " " + exception.name,
        # "description": exception.description
    })
    response.content_type = "application/json"

    return response


# @bp.app_errorhandler(400)
# def bad_request(error) -> Response:
#     return jsonify({"error": "400 Bad Request"}), 400


# @bp.app_errorhandler(404)
# def not_found(error) -> Response:
#     return jsonify({"error": "404 Not Found"}), 404


# @bp.app_errorhandler(500)
# def internal_server_error(error) -> Response:
#     return jsonify({"error": "500 Internal Server Error"}), 500


# @bp.app_errorhandler(405)
# def method_not_allowed(error) -> Response:
#     return jsonify({"error": "405 Method Not Allowed"}), 405
