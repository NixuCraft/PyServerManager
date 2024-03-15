import os
import shutil
import subprocess
from flask import request
from managers.porter import Porter
from instance import ServerInstance
from managers.servor import Servor
from variables import flask_app

@flask_app.route("/new", methods=["POST"])
def new_server():
    # Get data from request & perform checks
    data: dict[str, str] = request.get_json()

    game = data.get("game")
    if not game:
        return "Game attribute missing", 400
    
    version = data.get("version")
    if not version:
        return "Version attribute missing", 400
    
    game_version = f"{game}-{version}"
    game_folder = f"cache/servers/{game_version}"
    if not os.path.isdir(game_folder):
        return f"Missing server folder for {game_version}", 400
    
    map = data.get("map", "default")
    map_folder = f"cache/maps/{game_version}/{map}"
    if not os.path.isdir(map_folder):
        return f"Missing folder for map {map} of game {game_version}", 400

    # Get port
    port = Porter.get_use_random_port()

    # Copy files
    instance_folder = f"instances/{game_version}_{port}"
    shutil.copytree(game_folder, instance_folder)
    shutil.copytree(map_folder, f"{instance_folder}/world")

    # Patch properties file to match used port
    propfile = f"{instance_folder}/server.properties"
    with open(propfile, "r") as file: content = file.read()
    content = content.replace("server-port=25565", f"server-port={port}")
    with open(propfile, "w") as file: file.write(content)

    if os.name == 'nt':
        process = subprocess.Popen(["cmd.exe", "/c", "start.bat"], cwd=instance_folder, stdout=None)
    else:
        process = subprocess.Popen(["sh", f"start.sh"], cwd=instance_folder, stdout=subprocess.DEVNULL)

    Servor.add_instance(ServerInstance(game, map, version, port, process))

    return f"Started up new {game_version} game with map {map} at port {port}", 200