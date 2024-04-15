import logging
import shutil
import subprocess
from typing import Any
from utils import get_date_formatted
from variables import logs_server_dir

from managers.portmanager import PortManager
from datatypes.gametype import GameType

logger = logging.getLogger("datatypes.gameinstance")

class ServerInstance:
    gametype: GameType
    map: str | None
    args: dict[str, Any] # Note: this may get moved eg to the start.sh, for now staying here as it's simpler. May have minor overhead and complicate things a bit if running on different machines..
    port: int
    process: subprocess.Popen
    
    def __init__(self, gametype: GameType, map: str | None, args: dict[str, Any]):
        self.gametype = gametype
        self.map = map
        self.args = args
        logger.debug("Created ServerInstance: " + gametype.full_name + " with map " + str(map) + " & args " + str(args))

    def setup_and_run(self):
        # Get port
        self.port = PortManager.get_use_random_port()

        # Copy files
        instance_folder = f"instances/{self.gametype.full_name}_{self.port}"
        shutil.copytree(self.gametype.get_server_folder(), instance_folder)
        if self.map:
            shutil.copytree(f"{self.gametype.get_map_folder()}/{self.map}", f"{instance_folder}/world")

        # Copy plugins
        for plugin in self.gametype.plugins: 
            shutil.copy(f"cache/plugins/{plugin}.jar", f"{instance_folder}/plugins")

        # Patch properties file to match used port
        propfile = f"{instance_folder}/server.properties"
        with open(propfile, "r") as file: content = file.read()
        content = content.replace("server-port=25565", f"server-port={self.port}")
        with open(propfile, "w") as file: file.write(content)

        # Start server
        with open(f"{logs_server_dir}/[{get_date_formatted()}] {self.get_name()}.txt" , "a") as output_file:
            self.process = subprocess.Popen(["sh", "start.sh"], cwd=instance_folder, stdout=output_file, stderr=subprocess.STDOUT)

        logger.debug("Started server: " + self.get_name())

        
    def get_name(self):
        return f"{self.gametype.full_name}_{self.port}"

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
        PortManager.free_port(self.port)
        shutil.rmtree(f"instances/{self.get_name()}")