# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Provides the flask config options
"""
from os import getenv, urandom, path

import requests

PARENT_DIR = path.abspath(path.dirname(__file__))

class Config(object):
    HOST = "127.0.0.1"
    API_URL_PREFIX = "/v1"
    DEBUG = False

    # X-Shopify-Access-Token
    SHOPIFY_SCOPES = ['write_orders', 'read_customers']
    SHOPIFY_KEY = getenv("SHOPIFY_KEY")
    SHOPIFY_SECRET = getenv("SHOPIFY_SECRET")

    # Change based on mode
    ENVIRONMENT = "production"


class Development(Config):
    ENVIRONMENT = "development"
    DEBUG = True


class Test(Config):
    DEBUG = True
    TESTING = True
    ENVIRONMENT = "staging"


class Production(Config):
    # TODO: why do this?
    HOST = "0.0.0.0"


class Ngrok(Development):
    HOST = "nerevu.ngrok.io"
    SHOPIFY_REDIRECT_URI = f"https://nerevu.ngrok.io{Config.API_URL_PREFIX}/callback"
