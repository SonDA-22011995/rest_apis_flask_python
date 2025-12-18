from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError
)

from validator import (
    validate_name,
    validate_price
)


class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate_name)
    price = fields.Float(required=True, validate=validate_price)
    store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str(validate=validate_name)
    price = fields.Float(validate=validate_price)

    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field is required")



class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate_name)
