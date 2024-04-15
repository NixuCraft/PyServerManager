import logging
import subprocess


logger = logging.getLogger("datatypes.lobbyinstance")

class LobbyInstance:
    port: int
    process: subprocess.Popen
