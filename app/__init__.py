"""Initialize Flask app."""

from flask import Flask

from .models import db
from . import views


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///db_game.sqlite"
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(views.bp)

    return app
