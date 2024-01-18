from . import api_users_bp
from flask_restful import Api, Resource
from flask import request
from app.api_users.schemas import UserSchema
from app.auth.models import User
from app import db

api = Api(api_users_bp, errors=api_users_bp.errorhandler)


class UsersApi(Resource):
    def get(self):
        users = User.query.all()
        schema = UserSchema(many=True)

        return {"results": schema.dump(users)}

    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)
        db.session.add(user)
        db.session.commit()

        return {"msg": "User created", "user": schema.dump(user)}, 201


class UserApi(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        schema = UserSchema()

        return {"user": schema.dump(user)}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)

        db.session.add(user)
        db.session.commit()

        return {"msg": "User updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"msg": "User deleted"}


api.add_resource(UsersApi, '/users')
api.add_resource(UserApi, '/user/<int:user_id>')
