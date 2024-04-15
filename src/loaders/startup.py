from loaders.gamesloader import load_games_data, start_persistent_servers
from loaders.lobbyloader import load_lobbies_data
from managers.gametypemgr import GameTypeManager
from utils import cleanup_files


def perform_startup():
    # Pre cleanup/dirs creations
    cleanup_files()

    # Games data
    games_data = load_games_data()
    GameTypeManager._data_dict = games_data.data_dict
    GameTypeManager._data_object = games_data.data_object

    # Lobby
    # Note: some lobbies rely on the HTTP Api. If possible all servers (game ones too) should be started AFTER
    # the HTTP Api is set up (unlike rn where they're all started before).
    # This shouldn't cause issues because the HTTP api starts instantly and Popen takes no time too,
    # so they have time to start before the servers.
    lobbies_data = load_lobbies_data()

    # Start everything
    start_persistent_servers(games_data.to_start)

    for lobby in lobbies_data:
        lobby.setup_and_run()