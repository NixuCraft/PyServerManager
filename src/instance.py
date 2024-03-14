from dataclasses import dataclass
import subprocess


@dataclass
class ServerInstance:
    game: str
    map: str
    version: str
    port: int
    process: subprocess.Popen