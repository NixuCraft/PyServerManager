import os
import shutil
import subprocess
from flask import request
from managers.porter import Porter
from instance import ServerInstance
from managers.servor import Servor
from variables import flask_app

def error(message: str):
    return {
        "success": False,
        "error": message
    }, 400

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
        return error(f"Missing server folder for {game_version}")
    
    map = data.get("map", "default")
    map_folder = f"cache/maps/{game_version}/{map}"
    if not os.path.isdir(map_folder):
        return error(f"Missing folder for map {map} of game {game_version}")
    
    args = data.get("args", {})
    if not isinstance(args, dict):
        return error("Args not a dictionary")
    
    plugins: list[str] | str = data.get("plugins", [])
    plugin_folder = f"cache/plugins/{version}"
    if isinstance(plugins, str):
        plugins = [plugins]
    if len(plugins) > 0:
        if not os.path.isdir(plugin_folder):
            return error(f"Plugin(s) specified but no folder for {version} plugins")
        for plugin in plugins:
            if not os.path.isfile(f"{plugin_folder}/{plugin}.jar"):
                error(f"Plugin {plugin} doesn't exist for version {version}")
    
    # Get port
    port = Porter.get_use_random_port()

    # Copy files
    instance_folder = f"instances/{game_version}_{port}"
    shutil.copytree(game_folder, instance_folder)
    shutil.copytree(map_folder, f"{instance_folder}/world")

    # Copy plugins
    for plugin in plugins: 
        shutil.copy(f"{plugin_folder}/{plugin}.jar", f"{instance_folder}/plugins")

    # Patch properties file to match used port
    propfile = f"{instance_folder}/server.properties"
    with open(propfile, "r") as file: content = file.read()
    content = content.replace("server-port=25565", f"server-port={port}")
    with open(propfile, "w") as file: file.write(content)

    # Start server
    if os.name == 'nt':
        process = subprocess.Popen(["cmd.exe", "/c", "start.bat"], cwd=instance_folder, stdout=None)
    else:
        process = subprocess.Popen(["sh", f"start.sh"], cwd=instance_folder, stdout=subprocess.DEVNULL)

    # Add instance to manager
    instance = ServerInstance(game, map, version, plugins, args, port, process)
    Servor.add_instance(instance)

    return {
        "success": True,
        "game_version": game_version,
        "map": map,
        "name": instance.get_name(),
        "port": port
    }, 200