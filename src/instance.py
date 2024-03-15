from dataclasses import dataclass
import subprocess


@dataclass
class ServerInstance:
    game: str
    map: str
    version: str
    plugins: list[str]
    port: int
    process: subprocess.Popen
    
    def get_name(self):
        return f"{self.game}-{self.version}_{self.port}"

    def serialize(self):
        return {
            "game": self.game,
            "map": self.map,
            "version": self.version,
            "port": self.port,
            "pid": self.process.pid #why not
        }