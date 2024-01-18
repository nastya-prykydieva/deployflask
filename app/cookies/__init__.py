from flask import Blueprint

cookies = Blueprint("cookies", __name__, template_folder="templates/cookies")

from . import views