from managers.servor import Servor
from variables import flask_app

@flask_app.route("/list")
def list_servers():
    return [server.serialize() for server in Servor.get_instances_list()]
