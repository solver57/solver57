"""Initialize Flask app."""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os


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
    app.config.from_pyfile("config.py", silent=True)

    db.init_app(app)

    from .models import User
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    from .routes import main, school_game, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(school_game.bp)
    app.register_blueprint(auth.bp)

    return app
