from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    """Only to read data."""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True) # must be in JSON payload 
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemUpdateSchema(Schema):
    # optional
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int() # optional


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainItemSchema(), dump_only=True) # nested store

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    tags = fields.Nested(PlainTagSchema(), dump_only=True)
