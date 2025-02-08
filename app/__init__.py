# Flask 3.0 doesn't like Flask_Dropzone, or is it the other way around... either way...

from flask import Flask, url_for
import os
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from logging.config import dictConfig
from flask.logging import default_handler
import logging


load_dotenv()

bootstrap = Bootstrap5()

def create_app():
    app = Flask(__name__)
    
    root = logging.getLogger()
    root.addHandler(default_handler)
    
    app.logger.setLevel(logging.INFO)
    
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })
    
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
