from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import User
from app import db, requires_roles
import json

# CONFIG
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# ROUTES

# Displaying all users in the admin page.
@admin_blueprint.route('/admin', methods=['GET'])
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin.html', current_users=User.query.all())


@admin_blueprint.route('/contact')
def contact():
    return render_template('contact.html')


@admin_blueprint.route('/terms')
def terms():
    return render_template('terms.html')


@login_required
@requires_roles('admin')
@admin_blueprint.route('/update', methods=['POST', 'GET'])
def update():
    return render_template('update.html')
