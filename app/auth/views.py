from . import auth
from flask import request, render_template, redirect, url_for, flash, current_app
from app import db
from datetime import datetime
from app.auth.models import User
from .forms import RegistrationForm, LoginForm, ChangePasswordForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import os
import secrets


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are logged in.', category='success')
        return redirect(url_for('cookies.info'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are logged in.', category='success')
        return redirect(url_for('cookies.info'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', category='success')
            return redirect(url_for('cookies.info'))
        else:
            flash('Error! Please try again.', category='danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET'])
def logout():
    flash('You have been logged out.', category='success')
    logout_user()
    return redirect(url_for('auth.login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@auth.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response


@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your account has been updated!', category='success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@auth.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.commit()
            flash("Your password has been changed.", "success")
            return redirect(url_for('auth.account'))
        flash("Incorrect old password.", "danger")
        return redirect(url_for('auth.reset_password'))
    return render_template('password.html', form=form)


@auth.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users)
