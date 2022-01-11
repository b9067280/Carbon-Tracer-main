import logging
from datetime import datetime

import flask
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from app import db
from flask_login import login_required
from models import User
from users.forms import RegisterForm, LoginForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username already exists', "danger")
            return render_template('register.html', form=form)

        new_user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role='user')

        db.session.add(new_user)
        db.session.commit()

        # Send new user registered notification to security log file
        logging.warning('SECURITY - User registration [%s, %s]', form.email.data, request.remote_addr)

        # Sends user to login page and displays a message that a user has been created.
        return redirect(url_for('users.login')), flash('The user ' + new_user.email + ' has been created!', "success")

    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0
    # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded', "warning")

    form = LoginForm()

    if form.validate_on_submit():

        # increase login attempts by 1
        session['logins'] += 1

        user = User.query.filter_by(username=form.username.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            # if no match create appropriate error message based on login attempts
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded', "warning")
            elif session['logins'] == 2:
                flash('Please check your login details and try again. 1 login attempt remaining', "warning")
            else:
                flash('Please check your login details and try again. 2 login attempts remaining', "warning")

                # Send Invalid log in attempt notification to security log file
                logging.warning('SECURITY - Invalid log in attempt [%s, %s]', form.username.data, request.remote_addr)

            return render_template('login.html', form=form)

        session['logins'] = 0

        login_user(user)

        db.session.commit()

        # Send Log in notification to security log file
        logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.id, current_user.email, request.remote_addr)

        # direct to role appropriate page
        if current_user.role == 'admin':
            return redirect(url_for('users.profile'))
        else:
            return redirect(url_for('users.profile'))

    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
def logout():
    # Send Log out notification to security log file
    logging.warning('SECURITY - Log out [%s, %s, %s]', current_user.id, current_user.email, request.remote_addr)

    logout_user()
    return redirect(url_for('index'))


# View user profile
@users_blueprint.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


# View user's panel
@users_blueprint.route('/panel')
@login_required
def panel():
    return render_template('panel.html')
