from flask import request, jsonify, Blueprint, current_app, url_for, Response
from functools import wraps
import jwt
from models import User
from flask_sqlalchemy import Pagination
from typing import Callable, Tuple, Optional

bp = Blueprint("utils", __name__)

def with_token(f) -> Callable:
    @wraps(f)
    def decorator(*args, **kwargs) -> Callable:
        token = None

        print(request.headers)
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "401 Missing Token"}), 401
        
        user = None
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user = User.query.filter_by(public_id=data["public_id"]).first()
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return jsonify({"error": "401 Invalid Token"}), 401
        
        # invalid token -> non-existing user
        if not user:
            return jsonify({"error": "401 Invalid Token"}), 401

        return f(user, *args, **kwargs)

    return decorator


def build_pagination_urls(root_url: str, p: Pagination) -> Tuple[Optional[int], Optional[int], str, str]:
    prev_num = p.prev_num if p.has_prev else None
    next_num = p.next_num if p.has_next else None

    prev_url = root_url[:-1] + url_for("routes.get_movies", page=prev_num) if p.has_prev else ""
    next_url = root_url[:-1] + url_for("routes.get_movies", page=next_num) if p.has_next else ""

    return prev_num, next_num, prev_url, next_url


def add_pagination_headers(response: Response, pagination: Pagination, root_url: str) -> None:
    """
        Modifies input parameters
    """
    pagination_data = build_pagination_urls(request.root_url, pagination)

    response.headers["X-Total"] = pagination.total
    response.headers["X-Pages-Total"] = pagination.pages
    response.headers["X-Per-Page"] = pagination.per_page
    response.headers["X-Prev-Page"] = "" if not pagination_data[0] else pagination_data[0]
    response.headers["X-Next-Page"] = "" if not pagination_data[1] else pagination_data[1]
    response.headers["X-Prev-Page-Url"] = pagination_data[2]
    response.headers["X-Next-Page-Url"] = pagination_data[3]
