from flask import Flask
import os
from flask_bootstrap import Bootstrap5
from flask_dropzone import Dropzone

dropzone = Dropzone()
bootstrap = Bootstrap5()

def create_app():
    app = Flask(__name__)
    
    app.config.from_pyfile('./config/config.cfg')
    
    bootstrap.init_app(app)
    dropzone.init_app(app)
    
    from .main.main import main
    app.register_blueprint(main)