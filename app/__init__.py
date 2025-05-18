"""Initialize Flask app."""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    app.config.from_prefixed_env()

    db.init_app(app)

    from .models import User
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    from .routes import main, auth, solve, solve_api
    app.register_blueprint(main.bp)
    app.register_blueprint(solve.bp)
    app.register_blueprint(solve_api.bp)
    app.register_blueprint(auth.bp)

    return app
