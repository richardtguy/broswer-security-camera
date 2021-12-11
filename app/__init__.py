import os
from flask import Flask
from flask_socketio import SocketIO
import logging
from logging.handlers import RotatingFileHandler

# set up logging
if not os.path.exists('logs'):
	os.mkdir('logs')
file_handler = RotatingFileHandler('logs/flask.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
file_handler.setLevel(logging.DEBUG)

app = Flask(__name__)

socketio = SocketIO(logger=True)
logging.getLogger('socketio').addHandler(file_handler)

socketio.init_app(app)

from app import routes, signals
