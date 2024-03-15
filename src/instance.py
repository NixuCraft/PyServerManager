from dataclasses import dataclass
import subprocess
from typing import Any


@dataclass
class ServerInstance:
    game: str
    map: str
    version: str
    plugins: list[str]
    args: dict[str, Any]
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