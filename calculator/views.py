# Imports
from flask import Blueprint, render_template


# Config
calculator_blueprint = Blueprint('calculator', __name__, template_folder='templates')


@calculator_blueprint.route('/calculator')
def calculator():
    return render_template('calculator.html')


@calculator_blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    return render_template('update.html')


@calculator_blueprint.route('/<int:id>/delete')
def delete(id):

    return calculator()
