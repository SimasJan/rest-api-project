import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from models import StoreModel
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db

blp = Blueprint("Stores", __name__, description="Operations on stores.")

@blp.route('/store/<int:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required() #? you can call this endpoint unless you pass the access token
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}

@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema)
    def get(self):
        return StoreModel.query.all()

    @jwt_required() #? you can call this endpoint unless you pass the access token
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message='A store with that name already exists.')
        except SQLAlchemyError:
            abort(500, message="An error occured creating a store.")
        return store

        # for store in stores.values(): 
        #     if store_data['name'] == store.get('name'):
        #         abort(400, message=f"Store with name '{store_data['name']}' already exists.")

        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id} # include id in the dict
        # stores[store_id] = store 
        # return store
