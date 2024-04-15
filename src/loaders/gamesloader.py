from dataclasses import dataclass
import logging
import os
from typing import Any, cast

import pyjson5

from datatypes.instance.gameinstance import ServerInstance
from datatypes.gametype import GameType
from datatypes.persistentmeta import PersistentMeta
from managers.servermanager import ServerManager

logger = logging.getLogger("loaders.gamesloader")

@dataclass
class LoadedGames:
    data_object: dict[str, dict[str, GameType]]
    data_dict: dict[str, dict[str, dict[str, Any]]]
    to_start: list[GameType]

def load_games_data() -> LoadedGames:
    logger.info("Started loading data from config...")
    BASE_CONF_PATH = "config/games/"
    data_object = {}
    data_dict = {}
    to_start = []

    files = os.listdir(BASE_CONF_PATH)
    for game_name_json in files:
        game_name = game_name_json.replace(".json", "")
        data_dict[game_name] = {}
        data_object[game_name] = {}
        with open(BASE_CONF_PATH + game_name_json) as f:
            json_file: dict[str, dict] = pyjson5.loads(f.read())
        
        for variant, data in json_file.items():
            # Gen full dict & obj
            full_data = {"name": game_name, "variant": variant, **data}
            obj = GameType(**full_data)
            # Add to list for later treatment if persistent
            if obj.is_persistent(): to_start.append(obj)
            # Just add to normal dicts
            data_object[game_name][variant] = obj
            data_dict[game_name][variant] = obj.serialize() # cleanup dict before adding back to cache.
    
    logger.info("Done loading data from config.")

    return LoadedGames(data_dict, data_object, to_start)


def start_persistent_servers(to_start: list[GameType]):
    logger.info("Starting persistent servers...")
    for server in to_start:
        meta = cast(PersistentMeta, server.persistent_meta) # cast to make the type checker happy
        for i in range(meta.startup_instances):
            # Should be done in gametype init but disabled for debugging + just to be sure.
            check_res = server.check_main_folders_exist()
            if not check_res[0]:
                logger.warning("Persistent server for gametype " + server.full_name + " couldn't be started: " + check_res[1])
                continue
            instance = ServerInstance(server, None, meta.args)
            instance.setup_and_run()
            ServerManager.add_instance(instance)
            logger.debug("Persistent server " + instance.get_name() + " successfully started.")
        
    logger.info("Done starting persistent servers.")