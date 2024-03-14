from flask import request
from constants import flask_app

@flask_app.route("/new", methods=["POST"])
def new_server():
    data: dict[str, str] = request.get_json()
    data.get("game")
    return ""