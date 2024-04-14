from dataclasses import dataclass
import logging
import os
import shutil
import subprocess
from typing import Any

from managers.instances.porter import Porter
from datatypes.gametype import GameType

logger = logging.getLogger("datatypes.instance")

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
        self.port = Porter.get_use_random_port()

        # Copy files
        instance_folder = f"instances/{self.gametype.full_name}_{self.port}"
        print(instance_folder)
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
        if os.name == 'nt':
            self.process = subprocess.Popen(["cmd.exe", "/c", "start.bat"], cwd=instance_folder, stdout=None)
        else:
            self.process = subprocess.Popen(["sh", f"start.sh"], cwd=instance_folder, stdout=subprocess.DEVNULL)

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
        Porter.free_port(self.port)
        shutil.rmtree(f"instances/{self.get_name()}")