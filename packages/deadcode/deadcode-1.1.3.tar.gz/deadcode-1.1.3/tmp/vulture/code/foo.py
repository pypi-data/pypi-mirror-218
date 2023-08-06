from marshmallow import Schema, EXCLUDE

class MySchema(Schema):
    class Meta:
        unknown = EXCLUDE
