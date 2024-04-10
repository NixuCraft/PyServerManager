from flask import request
from managers.meta.gametypemgr import GameTypeManager
from variables import flask_app

@flask_app.route("/meta/all_game_types", methods=["GET"])
def game_types():
    return GameTypeManager.get_all_gametypes_json()