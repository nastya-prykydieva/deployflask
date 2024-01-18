from flask import Blueprint
from .models import TokenBlocklist

api_bp = Blueprint("api", __name__)

from . import views