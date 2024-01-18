from flask import Blueprint

todo_bp = Blueprint("todo_bp", __name__, template_folder="templates/todo")

from . import views
