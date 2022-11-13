from flask import Flask, Blueprint, render_template

projects = Blueprint('projects', __name__, template_folder='templates', static_folder='static')

@projects.route('/projects')
def projectsHome():
    return render_template('projects.html')