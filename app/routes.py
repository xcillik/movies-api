from flask import Blueprint, jsonify, request, Response, current_app
from models import Movie, db, MovieForm, UserForm, User
from werkzeug.security import generate_password_hash,check_password_hash
import uuid
import datetime
import jwt
from utils import *
import sys

bp = Blueprint("routes", __name__)

# root/index
@bp.route("/", methods=["GET", "POST"])
def index() -> Response:
    response = {
        "api": {
            "version": "1.0",
            "url": request.root_url + "movies",
            "user": {
                "generate_token": request.root_url + "users/token/generate",
                "register": {
                    "method": "POST",
                    "url": request.root_url + "users"
                },
                "index": request.root_url + "user"
            }
        }
    }

    return jsonify(response)


@bp.route("/user", methods=["GET"])
@with_token
def print_current_user(user) -> Response:
    return jsonify({
        "user_id": user.user_id,
        "username": user.username
    }), 200


# index users
@bp.route("/users", methods=["GET"])
def users() -> Response:
    users_paginated = User.query.paginate(page=None, per_page=None, error_out=True)
    users_list = []

    for movie in users_paginated.items:
        users_list.append(movie.jsonify())
    
    response = jsonify(users_list)

    add_pagination_headers(response, users_paginated, request.root_url)
    
    return response


# user register handler
@bp.route("/users", methods=["POST"])
def register() -> Response:
    form = UserForm(request.form)

    if not form.validate():
        return jsonify({"error": "400 Bad Request"}), 400
    
    username_already_exists = User.query.filter_by(username=form.username.data).count() > 0
    if username_already_exists:
        return jsonify({"error": "422 Unprocessable Content"}), 422
    
    hashed_password = generate_password_hash(form.password.data, method="scrypt")

    new_user = User(public_id=str(uuid.uuid4()), username=form.username.data, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return new_user.jsonify(), 201

# user login handler
@bp.route("/users/token/generate", methods=["POST"])
def login() -> Response:
    form = UserForm(request.form)

    if not form.validate():
        return jsonify({"error": "401 Unauthorized"}), 401
    
    user = User.query.filter_by(username=form.username.data).first()

    if not user or not check_password_hash(user.password, form.password.data):
        # wrong password
        return jsonify({"error": "401 Unauthorized"}), 401
    
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token = jwt.encode({
        "public_id": user.public_id,
        "expirates": exp.isoformat()
    }, current_app.config["SECRET_KEY"], "HS256")

    return jsonify({
        "token": token,
        "expirates": exp.isoformat()
    }), 200


# index movies
@bp.route("/movies", methods=["GET"])
def get_movies() -> Response:
    movies_paginated = Movie.query.paginate(page=None, per_page=None, error_out=True)
    movie_list = []

    for movie in movies_paginated.items:
        movie_list.append(movie.jsonify())
    
    response = jsonify(movie_list)

    add_pagination_headers(response, movies_paginated, request.root_url)
    
    return response


# get specific movie by id
@bp.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id) -> Response:
    movie = Movie.query.get(movie_id)
    
    if movie:
        return jsonify(movie.jsonify())
    
    return jsonify({"error": "404 Not Found"}), 404


# create a movie
@bp.route("/movies", methods=["POST"])
@with_token
def create_movie(user) -> Response:
    form = MovieForm(request.form)

    if not form.validate():
        return jsonify({"error": "400 Bad Request"}), 400
    
    new_movie = Movie(title=form.title.data, release_year=form.release_year.data, description=form.description.data, user_id=user.user_id)
    db.session.add(new_movie)
    db.session.commit()
    
    return new_movie.jsonify(), 201


# change movie attributes
@bp.route("/movies/<int:movie_id>", methods=["PUT"])
@with_token
def update_movie(user, movie_id) -> Response:
    form = MovieForm(request.form)

    if not form.validate():
        return jsonify({"error": "400 Bad Request"}), 400
    
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "404 Not Found"}), 404

    # user tries to change attributes of movie he did not create
    if movie.user_id != user.user_id:
        return jsonify({"error": "401 Unauthorized"}), 401
    
    movie.title = form.title.data
    movie.release_year = form.release_year.data
    movie.description = form.description.data

    db.session.commit()
    
    return movie.jsonify()


# delete movie by authorized user
@bp.route("/movies/<int:movie_id>", methods=["DELETE"])
@with_token
def delete_movie(user, movie_id) -> Response:
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "404 Not Found"}), 404
    
    # user tries to delete movie he did not create
    if movie.user_id != user.user_id:
        return jsonify({"error": "401 Unauthorized"}), 401
    
    Movie.query.filter_by(movie_id=movie.movie_id).delete()
    db.session.commit()

    return movie.jsonify(), 200
