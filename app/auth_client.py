from flask import g, request
from os import urandom
import hmac as hm
import hashlib

class AuthClient(object):
    def __init__(self, **kwargs):
        self.state
        self.shop
        self.hmac
        self.api_key = app.config['SHOPIFY_KEY']
        self.api_secret = app.config['SHOPIFY_SECRET']
        self.scope = ",".join(app.config['SHOPIFY_SCOPES'])
        self.redirect_uri = app.config['SHOPIFY_REDIRECT_URI']
        self.code
        self.token = {
            "access_token" = "",
            "scope" = "",
            # these online exist for offline
            "expires_in": "",
            "associated_user_scope": ""
            "associated_user": "",
        }

    def state():
        # state is the same as nonce
        self.state = urandom(24)


class MyAuthClient(AuthClient):
    def __init__(self, **kwargs):
        super().__init__()
        for k,v in kwargs.items():
            setattr(self, k, v)

    def authorization_url():
        self.auth_url =f"https://{self.shop}/admin/oauth/authorize?client_id={self.api_key}&scope={self.scope}&redirect_uri={self.redirect_uri}&state={self.nonce}"

    def check_state():
        # The nonce is the same one that your app provided to Shopify during step two.
        pass

    def check_hmac():
        # The hmac is valid. The HMAC is signed by Shopify as explained below, in Verification.
        args_no_hmac = ""
        for key, val in request.args.items():
            if key != 'hmac':
                args_no_hmac += f"{key}={val}&"
        args_no_hmac = args_no_hmac[:-1]
        signature = hm.new(bytes(self.api_secret , 'latin-1'), msg = bytes(args_no_hmac , 'latin-1'), digestmod = hashlib.sha256).hexdigest()
        if signature == self.hmac
        pass

    def check_hostname():
        # The hostname parameter is a valid hostname, ends with myshopify.com, and does not contain characters other than letters (a-z), numbers (0-9), dots, and hyphens.
        # You can use a regular expression like the following example to confirm that the hostname is valid:
            # /(https|http)\:\/\/[a-zA-Z0-9][a-zA-Z0-9\-]*\.myshopify\.com[\/]?/
        pass

    def query_shopify():
        # X-Shopify-Access-Token: {self.access_token["access_token"]} in header to make requests
        pass


#######################################################
# HELPER FUNCTIONS
#######################################################
def get_auth_client(prefix, **kwargs):
    auth_client_name = f"{prefix}_auth_client"

    if auth_client_name not in g:
        client = AuthClient(
            hmac=request.args.get('hmac'),
            shop=request.args.get('shop'),
        )

    return g.get(auth_client_name)
