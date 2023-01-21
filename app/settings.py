from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

STATIC_FOLDER = os.environ.get('static')
TEMPLATES_FOLDER = os.environ.get('templates')

SECRET_KEY = os.environ.get('secret')

FLASK_ENV = os.environ.get('FLASK_ENV')
FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
TESTING = os.environ.get('TESTING')

DROPZONE_ALLOWED_FILE_CUSTOM = os.environ.get('DROPZONE_ALLOWED_FILE_CUSTOM')
DROPZONE_ALLOWED_FILE_TYPE = os.environ.get('DROPZONE_ALLOWED_FILE_CUSTOM')
DROPZONE_MAX_FILE_SIZE = os.environ.get('DROPZONE_MAX_FILE_SIZE')