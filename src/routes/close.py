from flask import request
from managers.servor import Servor
from variables import flask_app

@flask_app.route("/close", methods=["POST"])
def close_server():
    data: dict[str, str] = request.get_json()
    instances = Servor.get_instances_list()

    hard = bool(data.get("hard", True))

    port = data.get("port")
    if port:
        port = int(port)
        for instance in instances:
            if instance.port == port:
                Servor.close_instance(instance, hard)
                return f"Successfully closed server {instance.get_name()} using port", 200
    
    pid = data.get("pid")
    if pid:
        pid = int(pid)
        for instance in instances:
            if instance.process.pid == pid:
                Servor.close_instance(instance, hard)
                return f"Successfully closed server {instance.get_name()} using pid", 200

    if not pid and not port:
        return "Neither a port nor a pid were provided. Please provide at least one", 400

    return "Couldn't find server to close", 500
