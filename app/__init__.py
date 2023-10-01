# Flask 3.0 doesn't like Flask_Dropzone, or is it the other way around... either way...

from flask import Flask, url_for
import os
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv

load_dotenv()

bootstrap = Bootstrap5()

def create_app():
    app = Flask(__name__)
    
    app.config.from_pyfile('settings.py')
    
    bootstrap.init_app(app)
    
    from .extensions import db
    db.init_app(app)
    
    from .main.main import main
    app.register_blueprint(main)
    
    from .aboutMe.aboutMe import aboutMe
    app.register_blueprint(aboutMe)
    
    from .projects.projects import projects
    app.register_blueprint(projects)
    
    
    return app
