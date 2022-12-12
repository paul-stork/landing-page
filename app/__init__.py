from flask import Flask
import os
from flask_bootstrap import Bootstrap5
from flask_dropzone import Dropzone
from dotenv import load_dotenv

load_dotenv()

dropzone = Dropzone()
bootstrap = Bootstrap5()

def create_app():
    app = Flask(__name__)
    
    app.config.from_pyfile('settings.py')
    
    bootstrap.init_app(app)
    dropzone.init_app(app)
    
    from .extensions import db
    db.init_app(app)
    
    from .main.main import main
    app.register_blueprint(main)
    
    from .aboutMe.aboutMe import aboutMe
    app.register_blueprint(aboutMe)
    
    from .projects.Projects import projects
    app.register_blueprint(projects)
    
    return app