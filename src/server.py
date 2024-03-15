from gevent.pywsgi import WSGIServer
from utils import cleanup_files
from variables import flask_app

from routes import new


if __name__ == "__main__":
    cleanup_files()
    print("Running server (prod)")
    http_server = WSGIServer(('', 57742), flask_app)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt: pass
    print("Keyboard interrupt detected, cleaning up")
    cleanup_files()