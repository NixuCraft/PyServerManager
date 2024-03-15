from flask import request
from managers.servor import Servor
from variables import flask_app

@flask_app.route("/info")
def server_info():
    port = request.get_json().get("port")
    if not port:
        return "No port specified", 400
    for server in Servor.get_instances_list():
        if server.port == port:
            return server.serialize()
    
    return "Server not found", 500
