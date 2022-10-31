from typing import Dict
from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

from db import db
import models
import configs

def create_app():
    """Create the app with the configs"""
    app = Flask(__name__)
    app.config.update(**configs.APP_CONFIGS)
    db.init_app(app)

    api = Api(app)

    # create db tables if not exists.
    with app.app_context():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    return app