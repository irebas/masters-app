from flask import Flask
from database import database

# blueprint import
from apps.app1.views import app1


def create_app():
    app = Flask(__name__)

    # setup with the configuration provided
    app.config.from_object('config.Config')

    # setup all our dependencies
    database.init_app(app)

    # register blueprint
    app.register_blueprint(app1)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(port=8000)

# https://codersdiaries.com/blog/flask-project-structure