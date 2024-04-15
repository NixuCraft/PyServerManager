from loaders.gamesloader import load_games_data, start_persistent_servers
from managers.gametypemgr import GameTypeManager
from utils import cleanup_files


def perform_startup():
    # Pre cleanup/dirs creations
    cleanup_files()

    # Games data
    games_data = load_games_data()
    GameTypeManager._data_dict = games_data.data_dict
    GameTypeManager._data_object = games_data.data_object
    start_persistent_servers(games_data.to_start)

    # Lobby
    