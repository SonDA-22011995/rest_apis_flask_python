from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError
)

from validator import (
    validate_name,
    validate_number
)

class AtLeastOneFieldSchema(Schema):
    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field is required")

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate_name)

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate_name)
    price = fields.Float(required=True, validate=validate_number)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate_name)

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class TagUpdateSchema(AtLeastOneFieldSchema):
    name = fields.Str(validate=validate_name)
    store_id = fields.Int(validate=validate_number)

class ItemUpdateSchema(AtLeastOneFieldSchema):
    name = fields.Str(validate=validate_name)
    price = fields.Float(validate=validate_number)
    store_id = fields.Int(validate=validate_number)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)