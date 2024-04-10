from dataclasses import dataclass
import shutil
import subprocess
from typing import Any

from managers.instances.porter import Porter
from datatypes.gametype import GameType


@dataclass
class ServerInstance:
    gametype: GameType
    map: str
    args: dict[str, Any] # Note: this may get moved eg to the start.sh, for now staying here as it's simpler. May have minor overhead and complicate things a bit if running on different machines..
    port: int
    process: subprocess.Popen
    
    def get_name(self):
        return f"{self.gametype}_{self.port}"

    def serialize(self):
        return {
            "gametype": self.gametype.serialize(),
            "map": self.map,
            "name": self.get_name(),
            "args": self.args,
            "port": self.port,
            "pid": self.process.pid #why not
        }
    
    def cleanup_after_close(self):
        Porter.free_port(self.port)
        shutil.rmtree(f"instances/{self.get_name()}")