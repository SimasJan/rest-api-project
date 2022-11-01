import json
from typing import Dict
from xmlrpc.client import Boolean
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

from blocklist import BLOCKLIST
import models
import configs
from db import db
import secrets

def create_app():
    """Create the app with the configs"""
    app = Flask(__name__)
    app.config.update(**configs.APP_CONFIGS)
    db.init_app(app)

    api = Api(app)
    jwt = JWTManager(app)

    # -- tokens
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload) -> Boolean:
        """Checks if the token is in the blocklist."""
        return jwt_payload['jti'] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({'description': 'The token has been revoked.', 'error': 'token_revoked'}), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({'description': 'The token is not fresh.', 'error': 'fresh_token_required'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload) -> Dict:
        """When token is expired, but is still tried to used to gain access."""
        return jsonify({'message': 'The token has expired.', 'error': 'token_expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error) -> Dict:
        """If token is invalid (i.e. when user tried to change it)."""
        return jsonify({'message': 'Signature verification failed.', 'error': 'invalid_token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error) -> Dict:
        """When no access token is provided."""
        return jsonify({'description': 'Request does not contain an access token.', 'error': 'authorization_required'}), 401

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity) -> Dict:
        """Returns whether the identity of the user is_admin or not. """
        # Look into the database and see whether the user is an admin
        if identity == 1:
            return {'is_admin': True}
        return {'is_admin': False}

    # create db tables if not exists.
    with app.app_context():
        db.create_all()

    # register resource endpoint blueprints
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app