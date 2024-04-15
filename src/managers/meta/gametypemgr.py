from logging import Logger
import logging
import os
from typing import cast

import pyjson5

from datatypes.gametype import GameType
from datatypes.gameinstance import ServerInstance
from datatypes.persistentmeta import PersistentMeta
from managers.instances.servor import Servor

logger = logging.getLogger("managers.meta.gametypemgr")


class GameTypeManager:
    _data_dict: dict[str, dict[str, dict]]
    _data_object: dict[str, dict[str, GameType]]
    _to_start: list[GameType]
    
    # Note: CONFIG LOADING SHOULD IDEALLY BE MOVED SOMEWHERE ELSE.
    @classmethod
    def _load_data(cls):
        logger.info("Started loading data from config...")
        BASE_CONF_PATH = "config/games/"
        cls._data_dict = {}
        cls._data_object = {}
        cls._to_start = []

        files = os.listdir(BASE_CONF_PATH)
        for game_name_json in files:
            game_name = game_name_json.replace(".json", "")
            cls._data_dict[game_name] = {}
            cls._data_object[game_name] = {}
            with open(BASE_CONF_PATH + game_name_json) as f:
                json_file: dict[str, dict] = pyjson5.loads(f.read())
            
            for variant, data in json_file.items():
                # Gen full dict & obj
                full_data = {"name": game_name, "variant": variant, **data}
                obj = GameType(**full_data)
                # Add to list for later treatment if persistent
                if obj.is_persistent(): cls._to_start.append(obj)
                # Just add to normal dicts
                cls._data_object[game_name][variant] = obj
                cls._data_dict[game_name][variant] = obj.serialize() # cleanup dict before adding back to cache.
        logger.info("Done loading data from config.")

    @classmethod
    def start_persistent_servers(cls):
        logger.info("Starting persistent servers...")
        for server in cls._to_start:
            meta = cast(PersistentMeta, server.persistent_meta) # cast to make the type checker happy
            for i in range(meta.startup_instances):
                # Should be done in gametype init but disabled for debugging + just to be sure.
                check_res = server.check_main_folders_exist()
                if not check_res[0]:
                    logger.warning("Persistent server for gametype " + server.full_name + " couldn't be started: " + check_res[1])
                    continue
                instance = ServerInstance(server, None, meta.args)
                instance.setup_and_run()
                Servor.add_instance(instance)
                logger.debug("Persistent server " + instance.get_name() + " successfully started.")
            
        logger.info("Done starting persistent servers.")
    
    @classmethod
    def get_all_gametypes_json(cls):
        return cls._data_dict
    
    @classmethod
    def get_gametype(cls, game: str, variant: str) -> GameType | None:
        try:
            return cls._data_object[game][variant]
        except Exception:
            return None
        

GameTypeManager._load_data()
