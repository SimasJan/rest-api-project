import json
from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

import uuid

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = 'Stores REST API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)
api.register_blueprint(StoreBlueprint)
api.register_blueprint(ItemBlueprint)


# @app.get('/store')
# def get_stores():
#     return jsonify( {'stores': list(stores.values())} )

# @app.get('/store/<string:id>')
# def get_store(id):
#     try: 
#         return stores[id]
#     except KeyError:
#         abort(404, message="Store not found.")
#         # return jsonify({'message': f'Store not found with name "{name}"'}), 404    

# @app.post('/store')
# def create_store():
#     store_data = request.get_json()
#     if 'name' not in store_data:
#         abort(400, message="Bad request. 'name' is a required in JSON payload.")
    
#     for store in stores.values():
#         if store_data['name'] == store.get('name'):
#             abort(400, message=f"Store with name '{store_data['name']}' already exists.")

#     store_id = uuid.uuid4().hex
#     new_store = {**store_data, "id": store_id} # include id in the dict
#     stores[store_id] = new_store
#     return new_store, 201

# @app.delete('/store/<string:id>')
# def delete_store(id):
#     try:
#         del stores[id]
#         return jsonify( {"message": "Store deleted."} )
#     except KeyError:
#         abort(404, message="Store not found.")

# # ITEMS

# @app.post('/item')
# def create_item():
#     item_data = request.get_json()
#     if (
#         "price" not in item_data
#         or "store_id" not in item_data
#         or "name" not in item_data
#     ):
#         abort(400, message="Bad request. One or all are missing in the JSON payload: 'price', 'store_id', 'name'.")
    
#     for item in items.values():
#         if (
#             item_data['name'] == item["name"]
#             and item_data['store_id'] == item["store_id"]
#         ):
#             abort(400, message=f"Item '{item['name']}' already exists.")

#     if item_data["store_id"] not in stores:
#         abort(404, message="Store not found.") 

#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item
#     return item, 201

# @app.get('/item')
# def get_all_items():
#     return jsonify( {'items': list(items.values())} )

# @app.get('/item/<string:item_id>')
# def get_item(item_id):
#     try:
#         return jsonify( items[item_id] )
#     except KeyError:
#         abort(404, message="Item not found.")

# @app.delete('/item/<string:item_id>')
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return jsonify( {"message": "Item deleted."} )
#     except KeyError:
#         abort(404, message="Item not found.")

# @app.put('/item/<string:item_id>')
# def update_item(item_id):
#     item_data = request.get_json()
#     if "price" not in item_data or "name" not in item_data:
#         abort(400, message="Bad request. Following values are required: 'price', 'name'.")
#     try:
#         item = items[item_id]
#         item |= item_data
#         return item
#     except KeyError:
#         abort(404, message="Item not found.")