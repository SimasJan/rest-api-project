from email import message
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("Items", __name__, description="Operations on items.")

@blp.route('/item/<int:item_id>')
class Item(MethodView):

    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        """Delete the item with the `item_id`, only if the user has admin identity."""
        jwt = get_jwt()
        if not jwt.get('is_admin'):
            abort(401, message='Admin privilege required.')
        
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """Update the item with the `item_data`.
        If item doesn't exist, the item is created.
        """
        item = ItemModel.query.get(item_id)
        
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        
        return item


@blp.route('/item')
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required() #? you can call this endpoint unless you pass the access token
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        """item_data is validated by the ItemSchema and passed through method only then."""
        item = ItemModel(**item_data) 
        
        try:
            db.session.add(item) # add many, undo (rollback), edit
            db.session.commit()  # commit once
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item in the database.")

        return item