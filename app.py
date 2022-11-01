from typing import Dict
from flask import Flask
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

    # create db tables if not exists.
    with app.app_context():
        db.create_all()

    # register resource endpoint blueprints
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app