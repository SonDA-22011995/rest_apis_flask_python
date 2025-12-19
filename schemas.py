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

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate_name)
    price = fields.Float(required=True, validate=validate_number)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate_name)

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str(validate=validate_name)
    price = fields.Float(validate=validate_number)
    store_id = fields.Int(validate=validate_number)

    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field is required")
