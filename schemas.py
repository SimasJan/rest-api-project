from marshmallow import Schema, fields

class ItemSchema(Schema):
    """Only to read data."""
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True) # must be in JSON payload 
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    # optional
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)