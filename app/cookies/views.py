from . import cookies
from flask import request, render_template, redirect, url_for, make_response, session, flash
from .forms import ChangePasswordForm
from flask_login import current_user, login_required
import json


def add_file_data():
    try:
        with open('app/file.json', 'r') as file:
            d = json.load(file)
        return d
    except FileNotFoundError:
        return flash("File doesn't exist!")


@cookies.route('/info')
@login_required
def info():
    form = ChangePasswordForm()
    username = current_user.username
    return render_template('info.html', form=form, username=username, cookies=request.cookies)


@cookies.route('/add_cookie', methods=['POST'])
def add_cookie():
    form = ChangePasswordForm()
    cookies = request.cookies
    key = request.form.get('key')
    value = request.form.get('value')
    max_age = int(request.form.get('max_age'))
    resp = make_response(render_template('info.html', username=current_user.username, cookies=cookies, form=form))
    resp.set_cookie(key, value, max_age=max_age)
    flash("Cookie is added! Please, refresh the page.", "success")
    return resp


@cookies.route('/remove_cookie', methods=['POST'])
def remove_cookie():
    form = ChangePasswordForm()
    cookies = request.cookies
    key = request.form.get('key')
    resp = make_response(render_template('info.html', username=current_user.username, cookies=cookies, form=form))
    if key in cookies:
        resp.delete_cookie(key)
        flash("Cookie is deleted! Please, refresh the page.", "success")
    return resp


@cookies.route('/remove_all_cookies', methods=['POST'])
def remove_all_cookies():
    form = ChangePasswordForm()
    cookies = request.cookies
    resp = make_response(render_template('info.html', username=current_user.username, cookies=cookies, form=form))
    for key in cookies.keys():
        print(key)
        if key != 'session':
            resp.delete_cookie(key)
    flash("All cookies are deleted!", "success")
    return resp


@cookies.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data
        file_data = add_file_data()
        try:
            json_password = file_data['password']
        except TypeError:
            flash("Error with data!", "error")
            raise SystemExit("Error with data!")
        if old_password == json_password:
            if new_password == confirm_password:
                session['password'] = new_password
                with open('app/file.json', "w") as file:
                    file_data['password'] = new_password
                    json.dump(file_data, file)
                    flash("Password was changed.", "success")
                    return redirect(url_for('cookies.info'))
        flash("Password was not changed.", "danger")
        return redirect(url_for('cookies.info'))
    return render_template('info.html', form=form)
