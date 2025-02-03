from marshmallow import Schema, fields, validate, ValidationError

# print(fields.Field.default_error_messages)

class Login(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'Email is required.'
        }
    )
    password = fields.String(
        required=True,
        error_messages={
            'required': 'Password is required.'
        }
    )
    

