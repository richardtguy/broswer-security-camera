import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Flask application configuration
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'itsasecret'

# Database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Email address for admin
ADMIN = os.environ.get('ADMIN')

# Email server configuration
MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
MAIL_SERVER=os.environ.get('MAIL_SERVER')
MAIL_PORT=os.environ.get('MAIL_PORT')
MAIL_USE_SSL=os.environ.get('MAIL_USE_SSL')

# Media file paths
UPLOADS_PATH = os.path.abspath(os.environ.get('UPLOADS_PATH')) or \
    os.path.abspath('.')
