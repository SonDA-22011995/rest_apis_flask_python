from marshmallow import ValidationError

def validate_name(value):
    if not isinstance(value, str):
        raise ValidationError("Must be a string")
    if not value.strip():
        raise ValidationError("Must not be empty or blank")


def validate_price(value):
    if value <= 0:
        raise ValidationError("Must be greater than zero")
