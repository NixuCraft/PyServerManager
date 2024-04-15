from managers.lobbiesmanager import LobbiesManager
from variables import flask_app

@flask_app.route("/meta/all_lobbies", methods=["GET"])
def game_types():
    return LobbiesManager.get_all_lobbies()