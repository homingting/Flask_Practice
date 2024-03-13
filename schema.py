from marshmallow import fields, Schema


class StoreSchema(Schema):
    id = fields.Int(dump_only=True)
    store_name = fields.Str(required=True)


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    item_name = fields.Str(required=True)
    item_price = fields.Float(required=True)


class TagSchema(Schema):
    id = fields.Int(dump_only=True)
    tag_name = fields.Str(required=True)


class FullStoreSchema(StoreSchema):
    items = fields.List(fields.Nested(ItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(TagSchema()), dump_only=True)


class FullItemSchema(ItemSchema):
    store = fields.Nested(StoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(TagSchema()), dump_only=True)


class UpdateItemSchema(ItemSchema):
    store_id = fields.Int(required=True)
    message = fields.Str(dump_only=True)
    update_item = fields.Nested(ItemSchema, dump_only=True)


class FullTagSchema(TagSchema):
    store = fields.Nested(StoreSchema, dump_only=True)
    items = fields.List(fields.Nested(ItemSchema()), dump_only=True)


class ItemTagSchema(Schema):
    message = fields.Str(dump_only=True)
    item = fields.Nested(ItemSchema())
    tag = fields.Nested(TagSchema())


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
