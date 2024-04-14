from dataclasses import dataclass, field
import os

from datatypes.persistentmeta import PersistentMeta

def bad(string: str) -> tuple[bool, str]:
    return (False, string)

def good(string: str) -> tuple[bool, str]:
    return (True, string)

@dataclass
class GameType:
    name: str
    variant: str
    full_name: str = field(init=False) 

    display_name: str
    room_icon: str
    
    min_protocol: int
    max_protocol: int

    min_players: int
    max_players: int

    plugins: list[str]
    
    persistent_meta: PersistentMeta | None = None 

    def __post_init__(self):
        # Gen full name
        self.full_name = f"{self.name}-{self.variant}"

        # Rework persistent meta to the right format
        if self.persistent_meta:
            self.persistent_meta = PersistentMeta(**self.persistent_meta) #type: ignore
        
        # res = self.check_main_folders_exist()
        # if not res[0]:
        #     raise Exception("Missing folders for gametype" + self.name + "-" + self.variant)
        # for debugging purposes, this is done on the new endpoint.
        # note that even if i do it on the new endpoint, i should still do it here just to make sure.

    def serialize(self):
        return {
            "name": self.name,
            "variant": self.variant,
            "display_name": self.display_name,
            "room_icon": self.room_icon,
            "min_protocol": self.min_protocol,
            "max_protocol": self.max_protocol,
            "min_players": self.min_players,
            "max_players": self.max_players,
            "plugins": self.plugins,
            "is_persistent": self.is_persistent()
        }

    def is_persistent(self):
        return self.persistent_meta != None
        
    def get_map_folder(self):
        return f"cache/maps/{self.name}"
    def get_server_folder(self):
        return f"cache/servers/{self.full_name}"
    
    def check_main_folders_exist(self) -> tuple[bool, str]:
        if not os.path.isdir(self.get_server_folder()):
            return bad(f"Missing server folder for {self.full_name}")
        
        if len(self.plugins) > 0:
            for plugin in self.plugins:
                if not os.path.isfile(f"cache/plugins/{plugin}.jar"):
                    bad(f"Plugin {plugin} doesn't exist.")
        
        return (True, "")

    def check_map_exists(self, map: str) -> tuple[bool, str]:
        if not os.path.isdir(self.get_map_folder()):
            return bad(f"Missing maps folder for game {self.name}")
        
        if not os.path.isdir(f"{self.get_map_folder()}/{map}"):
            return bad(f"Missing folder for map {map} of game {self.name}")
        return (True, "")

    def check_everything_exists(self, map: str) -> tuple[bool, str]:
        main_res = self.check_main_folders_exist()
        if not main_res[0]:
            return main_res

        map_res = self.check_map_exists(map)
        if not map_res[0]:
            return map_res
    
        return (True, "")