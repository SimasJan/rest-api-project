from typing import Dict
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
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

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """When token is expired, but is still tried to used to gain access."""
        return jsonify({'message': 'The token has expired.', 'error': 'token_expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """If token is invalid (i.e. when user tried to change it)."""
        return jsonify({'message': 'Signature verification failed.', 'error': 'invalid_token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """When no access token is provided."""
        return jsonify({'description': 'Request does not contain an access token.', 'error': 'authorization_required'}), 401

    # create db tables if not exists.
    with app.app_context():
        db.create_all()

    # register resource endpoint blueprints
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app