from flask import Flask, Blueprint, render_template

aboutMe = Blueprint('aboutMe', __name__, template_folder='templates', static_folder='static')

@aboutMe.route('/aboutme')
def aboutme():
    return render_template('aboutMe.html')