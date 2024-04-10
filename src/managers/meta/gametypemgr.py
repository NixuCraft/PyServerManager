import os

import pyjson5

from datatypes.gametype import GameType


class GameTypeManager:
    _data_dict: dict[str, dict[str, dict]]
    _data_object: dict[str, dict[str, GameType]]
    
    @classmethod
    def _load_data(cls):
        BASE_CONF_PATH = "config/games/"
        cls._data_dict = {}
        cls._data_object = {}

        files = os.listdir(BASE_CONF_PATH)
        for game_name_json in files:
            game_name = game_name_json.replace(".json", "")
            cls._data_dict[game_name] = {}
            cls._data_object[game_name] = {}
            with open(BASE_CONF_PATH + game_name_json) as f:
                json_file: dict[str, dict] = pyjson5.loads(f.read())
            
            for variant, data in json_file.items():
                full_data = {"name": game_name, "variant": variant, **data}
                cls._data_object[game_name][variant] = GameType(**full_data)
                cls._data_dict[game_name][variant] = full_data
    
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