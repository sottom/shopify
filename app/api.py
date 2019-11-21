# -*- coding: utf-8 -*-
"""
    app.api
    ~~~~~~~

    Provides additional api endpoints
"""
import re
import os
import json

from flask import Blueprint
from flask import current_app as app
from flask import redirect, request, session, url_for

import requests
from app.utils import get_common_rel, jsonify
from config import Config
import hmac as hm
import hashlib

# TODO: why do I get an error when doing 'auth_client' without the '.'?
from .auth_client import get_auth_client

blueprint = Blueprint("API", __name__)
PREFIX = Config.API_URL_PREFIX
nonce = ''

def get_request_base():
    return request.base_url.split("/")[-1].split("?")[0]


def get_resource_name(rule):
    """ Returns resourceName from endpoint

    Args:
        rule (str): the endpoint path (e.g. '/v1/data')

    Returns:
        (str): the resource name

    Example:
        >>> rule = '/v1/data'
        >>> get_resource_name(rule)
        'data'
    """
    url_path_list = [p for p in rule.split("/") if p]
    return url_path_list[:2].pop()


def get_params(rule):
    """ Returns params from the url

    Args:
        rule (str): the endpoint path (e.g. '/v1/data/<int:id>')

    Returns:
        (list): parameters from the endpoint path

    Example:
        >>> rule = '/v1/random_resource/<string:path>/<status_type>'
        >>> get_params(rule)
        ['path', 'status_type']
    """
    # param regexes
    param_with_colon = r"<.+?:(.+?)>"
    param_no_colon = r"<(.+?)>"
    either_param = param_with_colon + r"|" + param_no_colon

    parameter_matches = re.findall(either_param, rule)
    return ["".join(match_tuple) for match_tuple in parameter_matches]


def get_rel(href, method, rule):
    """ Returns the `rel` of an endpoint (see `Returns` below).

    If the rule is a common rule as specified in the utils.py file, then that rel is returned.

    If the current url is the same as the href for the current route, `self` is returned.

    Args:
        href (str): the full url of the endpoint (e.g. https://alegna-api.nerevu.com/v1/data)
        method (str): an HTTP method (e.g. 'GET' or 'DELETE')
        rule (str): the endpoint path (e.g. '/v1/data/<int:id>')

    Returns:
        rel (str): a string representing what the endpoint does

    Example:
        >>> href = 'https://alegna-api.nerevu.com/v1/data'
        >>> method = 'GET'
        >>> rule = '/v1/data'
        >>> get_rel(href, method, rule)
        'data'

        >>> method = 'DELETE'
        >>> get_rel(href, method, rule)
        'data_delete'

        >>> method = 'GET'
        >>> href = 'https://alegna-api.nerevu.com/v1'
        >>> rule = '/v1
        >>> get_rel(href, method, rule)
        'home'
    """
    if href == request.url and method == request.method:
        rel = "self"
    else:
        # check if route is a common route
        resourceName = get_resource_name(rule)
        rel = get_common_rel(resourceName, method)

        # add the method if not common or GET
        if not rel:
            rel = resourceName
            if method != "GET":
                rel = f"{rel}_{method.lower()}"

        # get params and add to rel
        params = get_params(rule)
        if params:
            joined_params = "_".join(params)
            rel = f"{rel}_{joined_params}"

    return rel


def gen_links():
    url_root = request.url_root.rstrip("/")
    # loop through endpoints
    for r in app.url_map.iter_rules():
        # don't show some routes
        if "static" not in r.rule and "callback" not in r.rule and r.rule != "/":
            # loop through relevant methods
            for method in r.methods - {"HEAD", "OPTIONS"}:
                href = url_root + r.rule
                rel = get_rel(href, method, r.rule)
                yield {"rel": rel, "href": href, "method": method}


def sort_links(links):
    return sorted(links, key=lambda link: link["href"])

def get_nonce():
    global nonce
    nonce = os.urandom(24)
    return nonce


###########################################################################
# ROUTES
###########################################################################
@blueprint.route("/")
def index():
    return redirect(url_for(".home"))


@blueprint.route(PREFIX)
def home():
    response = {
        "description": "Returns API documentation",
        "message": "Welcome to the Alegna Commission Calculator API!",
        "links": sort_links(gen_links()),
    }

    return jsonify(**response)


@blueprint.route(f"{PREFIX}/auth")
def auth():
    # shop = request.args.get('shop')
    # hmac = request.args.get('hmac')
    auth_client = get_auth_client("SHOPIFY")
    auth_client.check_hmac(request.args)

    return redirect(auth_client.authorization_url())


@blueprint.route(f"{PREFIX}/callback")
def callback():
    # hmac = request.args.get('hmac')
    # shop = request.args.get('shop')
    state = request.args.get('state')
    code = request.args.get('code')

    # shop and hmac need to be saved in the cache or something
    client = get_auth_client("SHOPIFY")
    if not all([client.check_state(state), client.check_hmac(request.args)]):
        # raise Exception('not all tests passed')
        pass

    client.code = code
    client.fetch_token()

    return json.dumps(client.token)
