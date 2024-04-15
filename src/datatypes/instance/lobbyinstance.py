import logging
import re
import subprocess
from variables import logs_server_dir

from datatypes.instance.instance import Instance
from managers.portmanager import PortManager


logger = logging.getLogger("datatypes.instance.lobbyinstance")

class LobbyInstance(Instance):
    name: str
    display_name: str
    port: int
    process: subprocess.Popen

    def __init__(self, name: str, display_name: str):
        self.name = "lobby_" + name
        self.display_name = display_name
        logger.debug(f"Created LobbyInstance {display_name}")
    
    def serialize(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "port": self.port,
            "pid": self.process.pid
        }

    def setup_and_run(self):
        self.port = PortManager.get_use_random_port()

        # Copy files
        instance_folder = f"instances_lobbies/{self.name}"

        propfile = f"{instance_folder}/server.properties"
        with open(propfile, "r") as file: content = file.read()    
        content = re.sub(r'server-port=\d{4,5}', f'server-port={self.port}', content)
        with open(propfile, "w") as file: file.write(content)


        # Start server
        with open(f"{logs_server_dir}/lobbies/{self.get_name()}.txt" , "a") as output_file:
            self.process = subprocess.Popen(["sh", "start.sh"], cwd=instance_folder, stdout=output_file, stderr=subprocess.STDOUT)

    def get_name(self):
        return f"{self.name}_{self.port}"