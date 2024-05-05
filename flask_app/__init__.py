# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename


# stdlib
from datetime import datetime
import os
import urllib.parse

# local
from .client import MovieClient

if os.getenv('API_KEY'):
    API_KEY = os.getenv('API_KEY')

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
movie_client = MovieClient(API_KEY)

from .users.routes import users
from .stocks.routes import movies

def custom_404(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["MONGODB_HOST"] = os.getenv("MONGO_URI")
    if test_config is not None:
        app.config.update(test_config)

    parsed = urllib.parse.urlparse(os.getenv("MONGO_URI"))

    app.config["MONGODB_SETTINGS"] = {
        'db': 'Cluster0',  # Removes the leading '/' from the path
        'host': parsed.hostname,
        'port': parsed.port,
        'username': parsed.username,
        'password': parsed.password
    }

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(movies)
    app.register_error_handler(404, custom_404)

    login_manager.login_view = "users.login"

    return app
