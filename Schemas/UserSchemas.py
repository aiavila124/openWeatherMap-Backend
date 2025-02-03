from marshmallow import Schema, fields, validate, ValidationError

# print(fields.Field.default_error_messages)

class GetUserSchema(Schema):
    user_id = fields.Integer(required=False)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    password = fields.String(required=False)
    email = fields.Email(required=False)
    active = fields.Integer(required=False)

class CreateUserSchema(Schema):
    first_name = fields.String(
        required=True,
        error_messages={
            'required': 'First name is required.'
        }
    )
    last_name = fields.String(
        required=True,
        error_messages={
            'required': 'Last name is required.'
        }
    )
    password = fields.String(
        required=True,
        error_messages={
            'required': 'Password is required.'
        },
        # validate=validate.Regexp(
        #     r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*!])[A-Za-z\d@#$%^&*!]{8,}$',
        #     error= 'Password format is incorrect.'
        # )
    )
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'Email is required.'
        }
    )
    active = fields.Integer(required=False)


class UpdateUserSchema(Schema):
    user_id = fields.Integer(
        required=True,
        error_messages={
            'required': 'User id is required.'
        }
    )
    first_name = fields.String(
        required=False
    )
    last_name = fields.String(required=False)
    password = fields.String(
        required=False,
        validate=validate.Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*!])[A-Za-z\d@#$%^&*!]{8,}$',
            error= 'Password format is incorrect.'
        )
    )
    email = fields.Email(required=False)
    active = fields.Integer(required=False)

class DeleteUserSchema(Schema):
    user_id = fields.Integer(required=True)
