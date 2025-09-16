from flask import Flask, Blueprint, render_template

contactMe = Blueprint('contactMe', __name__, template_folder='templates', static_folder='static')

@contactMe.route('/contactme')
def contactme():
    return render_template('contactMe.html')