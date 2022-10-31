from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel, TagModel
from schemas import StoreSchema

blp = Blueprint("Tags", "tags", description="Operations on tags.")

@blp.route('/store/<string:store_id>/tag')
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """Get all the tags associated with the store."""
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        """Add the tag(s) to the store with the store_id."""
        #NOTE: Don't need it as the models contain already the relationship validation.
        # if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data['name']).first():
        #     abort(400, message="Tag with name: '{}' already exists in the store with id: '{}'".format(
        #         tag_data['name'], tag_data['store_id']))

        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag

@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
        

    