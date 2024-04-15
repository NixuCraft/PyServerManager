from managers.servermanager import ServerManager
from variables import flask_app

@flask_app.route("/instances/list")
def list_servers():
    return [server.serialize() for server in ServerManager.get_instances_list()]
