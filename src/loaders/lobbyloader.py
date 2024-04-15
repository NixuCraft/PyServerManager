import logging
import os
import pyjson5

from datatypes.instance.lobbyinstance import LobbyInstance

logger = logging.getLogger("loaders.lobbyloader")

def load_lobbies_data() -> list[LobbyInstance]:
    BASE_CONF_PATH = "config/lobby/"
    files = os.listdir(BASE_CONF_PATH)
    for lobby_name_json in files:
        lobbies: list[LobbyInstance] = []
        with open(BASE_CONF_PATH + lobby_name_json) as f:
            json_file: dict[str, str] = pyjson5.loads(f.read())
        
        obj = LobbyInstance(**json_file)
        lobbies.append(obj)
    
    logger.info("Done loading data from config.")

    return lobbies