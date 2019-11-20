# -*- coding: utf-8 -*-
"""
    app
    ~~~

    Provides the flask application
"""
import config

from os import getenv, path
from flask import Flask, redirect, request
from dotenv import load_dotenv

load_dotenv(path.join(config.PARENT_DIR, '.env'))

def create_app(config_mode=None, config_file=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(api)

    if config_mode:
        app.config.from_object(getattr(config, config_mode))
    elif config_file:
        app.config.from_pyfile(config_file)
    else:
        app.config.from_envvar("APP_SETTINGS", silent=True)

    return app


# put at bottom to avoid circular reference errors
from app.api import blueprint as api  # noqa
