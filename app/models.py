from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, IntegerField, validators
from typing import Any, Dict

db = SQLAlchemy()


class MovieForm(Form):
    title = StringField("Title", validators=[validators.DataRequired(), validators.length(max=256)])
    release_year = IntegerField("Release Year", validators=[validators.DataRequired()])
    description = StringField("Description", validators=[validators.DataRequired(), validators.length(max=1024)])


class UserForm(Form):
    username = StringField("Username", validators=[validators.DataRequired(), validators.length(max=256)])
    password = StringField("Password", validators=[validators.DataRequired(), validators.length(max=1024)])


class User(db.Model):
    """
    TODO:
    - add token limit
    - token limit check
    """
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(80))

    def __repr__(self) -> str:
        return f"<User {self.user_id}, {self.public_id}, {self.username}, {self.password}>"
    
    def jsonify(self)  -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "username": self.username
        }


class Movie(db.Model):
    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id, ondelete="RESTRICT"), nullable=False)

    def __repr__(self) -> str:
        return f"<Movie {self.movie_id}, {self.title}, {self.release_year}, {self.description[:40]}>"

    def jsonify(self) -> Dict[str, Any]:
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "release_year": self.release_year,
            "description": self.description,
            "user_id": self.user_id
        }
