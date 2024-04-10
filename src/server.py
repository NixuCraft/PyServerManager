from gevent.pywsgi import WSGIServer
from managers.instances.servor import Servor
from utils import cleanup_files
from variables import flask_app

from routes.instances import new, list, close
from routes.games import all_game_types

if __name__ == "__main__":
    cleanup_files()
    print("Running server (prod)")
    http_server = WSGIServer(('', 57742), flask_app)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt: pass
    print("Keyboard interrupt detected, cleaning up")
    Servor.close_all_instances()
    cleanup_files()