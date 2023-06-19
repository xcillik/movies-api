from flask import Flask, jsonify
from models import db, Movie, User
import os
from werkzeug.security import generate_password_hash,check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))


def app_init() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "430d0a6205bbd7c650f0660c2b082e68"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()

    import error_handling
    app.register_blueprint(error_handling.bp)
    import routes
    app.register_blueprint(routes.bp)
    import utils
    app.redirect(utils.bp)

    return app


def try_seed(app: Flask) -> None:
    if len(Movie.query.all()) > 0:
        return
    
    u1 = User(username="john", password=generate_password_hash("0000", method="scrypt"))
    u2 = User(username="mark", password=generate_password_hash("1111", method="scrypt"))
    db.session.add(u1)
    db.session.add(u2)

    m1 = Movie(title="The Matrix", description="The Matrix is a computer-generated gream world...", release_year=1999, user_id=1)
    m2 = Movie(title="The Matrix Reloaded", description="Continuation of the cult classic The Matrix...", release_year=2003, user_id=2)
    db.session.add(m1)
    db.session.add(m2)

    for i in range(40):
        db.session.add(Movie(title="The Movie " + str(i), description="Lorem ipsum dolor sit amet...", release_year=2005, user_id=1))

    db.session.commit()


def main() -> None:
    app = app_init()

    with app.app_context():
        try_seed(app)

    app.run(debug=True, host="0.0.0.0", port=80)


if __name__ == "__main__":
    main()