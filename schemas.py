from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    """Only to read data."""
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True) # must be in JSON payload 
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    # optional
    name = fields.Str()
    price = fields.Float()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    # nested store
    store = fields.Nested(PlainItemSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)