from marshmallow import validate, validates_schema, ValidationError
from marshmallow.fields import String
from app.auth.models import User
from app import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    username = String(required=True, validate=[validate.Length(min=2)], error_messages={
        "required": "The name is required",
        "invalid": "The name is invalid and needs to be a string",
    })
    email = String(required=True, validate=[validate.Email()])
    password = String(required=True, validate=[validate.Length(min=6)])

    @validates_schema
    def validate_username(self, data, **kwargs):
        username = data.get("username")

        if User.query.filter_by(username=username).count():
            raise ValidationError(f"Username {username} already exists.")

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get("email")

        if User.query.filter_by(email=email).count():
            raise ValidationError(f"Email {email} already exists.")

    class Meta:
        model = User
        load_instance = True
        exclude = ["id", "password_hash"]
