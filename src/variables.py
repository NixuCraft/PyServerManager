from datetime import datetime
from flask import Flask

flask_app = Flask(__name__)

logs_server_dir = "logs_servers/" + datetime.now().strftime("%Y-%m-%d_%Hh%M")