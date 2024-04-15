import logging

from datatypes.gametype import GameType
from datatypes.instance.lobbyinstance import LobbyInstance
logger = logging.getLogger("managers.lobbiesmanager")


class LobbiesManager:
    # TODO: LOAD LOBBIES ON THE FLY W A REQUEST (not at all required for now)
    _lobby_instances: list[LobbyInstance]

    @classmethod
    def get_all_lobbies(cls):
        return [x.serialize() for x in cls._lobby_instances]
    
    @classmethod
    def get_lobby_from_name(cls, name: str) -> LobbyInstance | None:
        for lobby in cls._lobby_instances:
            if lobby.name == name:
                return lobby
        
    @classmethod
    def get_lobby_from_port(cls, port: int) -> LobbyInstance | None:
        for lobby in cls._lobby_instances:
            if lobby.port == port:
                return lobby
