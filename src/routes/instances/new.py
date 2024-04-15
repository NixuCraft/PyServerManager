import logging
import os
import random
from flask import request
from datatypes.instance.gameinstance import ServerInstance
from managers.servermanager import ServerManager
from managers.gametypemgr import GameTypeManager
from variables import flask_app

logger = logging.getLogger("routes.instances.new")

def error(message: str):
    logger.info("return @ " + message)
    return {
        "success": False,
        "error": message
    }, 400

@flask_app.route("/instances/new", methods=["POST"])
def new_server():
    # Get data from request & perform checks
    data: dict[str, str] = request.get_json()

    game = data.get("game")
    if not game:
        return error("Game attribute missing")
    
    variant = data.get("variant")
    if not variant:
        return error("Version attribute missing")

    gametype = GameTypeManager.get_gametype(game, variant)
    if not gametype:
        return error("Game/variant combination isn't related to any defined gametype.")
    
    map_cache = f"cache/maps/{game}"
    
    map = data.get("map", variant)
    if map == None:
        map = variant
    elif map == "RANDOM":
        maps = os.listdir(map_cache)
        if len(maps) == 0:
            return error(f"Map random specified for {game}, but there are no maps in the maps folder")
        map = random.choice(maps)
    
    check_res = gametype.check_everything_exists(map)
    if not check_res[0]:
        return error(check_res[1])

    
    args = data.get("args", {})
    if not isinstance(args, dict):
        return error("Args not a dictionary")
    
    instance = ServerInstance(gametype, map, args)
    instance.setup_and_run()
    ServerManager.add_instance(instance)


    return {
        "success": True,
        "map": map,
        "name": instance.get_name(),
        "port": instance.port
    }, 200