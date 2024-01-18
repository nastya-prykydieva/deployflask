from flask import Blueprint

portfolio = Blueprint("portfolio", __name__, template_folder="templates/portfolio")

from . import views
