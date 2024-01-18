from flask import Blueprint, jsonify
from marshmallow import ValidationError

api_users_bp = Blueprint("api_users", __name__)


@api_users_bp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400


from . import views
