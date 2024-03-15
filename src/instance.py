from dataclasses import dataclass
import subprocess
from typing import Any


@dataclass
class ServerInstance:
    game: str
    map: str
    version: str
    plugins: list[str]
    args: dict[str, Any] # Note: this may get moved eg to the start.sh, for now staying here as it's simpler. May have minor overhead and complicate things a bit if running on different machines..
    port: int
    process: subprocess.Popen
    
    def get_name(self):
        return f"{self.game}-{self.version}_{self.port}"

    def serialize(self):
        return {
            "game": self.game,
            "map": self.map,
            "version": self.version,
            "plugins": self.plugins,
            "args": self.args,
            "port": self.port,
            "pid": self.process.pid #why not
        }