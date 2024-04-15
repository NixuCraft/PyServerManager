import logging

from datatypes.gametype import GameType
logger = logging.getLogger("managers.meta.gametypemgr")


class GameTypeManager:
    _data_dict: dict[str, dict[str, dict]]
    _data_object: dict[str, dict[str, GameType]]

    @classmethod
    def get_all_gametypes_json(cls):
        return cls._data_dict
    
    @classmethod
    def get_gametype(cls, game: str, variant: str) -> GameType | None:
        try:
            return cls._data_object[game][variant]
        except Exception:
            return None
        
