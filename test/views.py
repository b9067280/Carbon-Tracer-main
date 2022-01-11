# Imports
from flask import Blueprint, render_template

# Config
quiz_blueprint = Blueprint('test', __name__, template_folder='templates')


@quiz_blueprint.route('/test')
def test():
    return render_template('test.html')
