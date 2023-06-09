from flask import Flask
from app.views import bp_app
import app.database


def create_app():
    app = Flask(__name__)

    # setup with the configuration provided
    app.config.from_object('config.Config')

    # setup all our dependencies
    database.init_app(app)

    # register blueprint
    app.register_blueprint(bp_app)

    return app

# https://codersdiaries.com/blog/flask-project-structure
