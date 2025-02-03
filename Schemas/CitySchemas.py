from marshmallow import Schema, fields, validate, ValidationError


class GetCitySchema(Schema):
    city_id = fields.Integer(required=False)
    name = fields.String(required=False)
    state_id = fields.Integer(required=False)
    limit = fields.Integer(required=False)
    offset = fields.Integer(required=False)

class CreateCitySchema(Schema):
    name = fields.String(required=True)
    state_id = fields.Integer(required=True)

class UpdateCitySchema(Schema):
    city_id = fields.Integer(required=True)
    name = fields.String(required=False)
    state_id = fields.Integer(required=False)

class DeleteCitySchema(Schema):
    city_id = fields.Integer(required=True)
