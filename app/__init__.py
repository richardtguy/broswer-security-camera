import os
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import RotatingFileHandler

# set up logging
if not os.path.exists('logs'):
	os.mkdir('logs')
file_handler = RotatingFileHandler('logs/flask.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
file_handler.setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
login.login_message_category = 'warn'
mail = Mail()

socketio = SocketIO(logger=True)
logging.getLogger('socketio').addHandler(file_handler)

socketio.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
login.init_app(app)
mail.init_app(app)

# add cli commands
from app.commands import create_user, delete_user
app.cli.add_command(create_user)
app.cli.add_command(delete_user)

from app import routes, signals, models, auth
