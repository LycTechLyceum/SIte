from flask import Blueprint, render_template, request, flash, session, url_for, redirect, send_from_directory
import os
from validate_email import validate_email  # для проверки имейла на существование и корректность
import requests
mn = Blueprint('main_pages', __name__)
URL = 'https://lyctech-db-test.herokuapp.com/api/'  # часть api для доступа к хероку


@mn.route('/logged')
def logged():
    # получаем информацию о пользователе по логину в сессии
    user = {"initials": session['initials']}

    return render_template('main-after-login.html', user=user)


@mn.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            check_password = requests.get(URL + 'check-password', json={'login': username, 'password': password}).json()
            # print(check_password)
            if check_password['ans']:  # проверяем логин и пароль
                # получаем данные о пользователе по логину и отправляем его на страницу
                # name = "Tim"
                # surname = "Smirnov"
                # user = {"initials": name + " " +surname}
                user_info = requests.get(URL + 'user-data', json={'login': username}).json()
                # print(user_info)
                session.clear()
                session['login'] = username
                session['initials'] = user_info['name']
                user = {"initials": session['initials']}
                return render_template("main-after-login.html", user=user)
        flash(error)

    return render_template('login.html')


@mn.route('/signup', methods=('GET', 'POST'))
def signup():  # получаем все, все, все данные :)
    if request.method == 'POST':
        username = str(request.form['login'])
        password = str(request.form['password'])
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            user = requests.post(URL + 'user', json={"name": username, "surname": username, "grade": username, "id_pos": 1
                                            ,'login': username, 'password': password}).json()
            # print(user)
            return redirect(url_for('main_pages.login'))

        flash(error)
    return render_template('register.html')


@mn.route('/logout')  # чистим сессию и переходим на страницу без регистрации
def logout():
    session.clear()
    return redirect(url_for('main_pages.login'))


@mn.route('/practicum')  # чистим сессию и переходим на страницу без регистрации
def practicum():
    # получаем данные о пользователе по логину и отправляем его на страницу
    # practices = requests.get(URL + 'practices').json()
    # print(practices)
    user = {"initials": session['initials']}
    practices = requests.get(URL + 'practices').json()
    # print(practices)
    # practices = {1: {"name": "First", "date": "10.03.2022"}, 2: {"name": "Second", "date": "10.04.2022"},
    #              3: {"name": "Second", "date": "10.05.2022"}}
    print(practices)
    return render_template('practicum.html', user=user, practices=practices)


@mn.route('/reg-to-practicum')  # чистим сессию и переходим на страницу без регистрации
def reg_to_practicum():

    user = {"initials": session['initials']}
    return render_template('reg-to-practicum.html', user=user)


@mn.route('/email-is-valid')  # чистим сессию и переходим на страницу без регистрации
def email_is_valid():
    user = {"initials": session['initials']}
    return render_template('email-is-true.html', user=user)


@mn.route('/project', methods=('GET', 'POST'))  # чистим сессию и переходим на страницу без регистрации
def project():
    user = {"initials": session['initials']}

    # if request.method == 'POST':
    #     email = request.form['email']
    #     # about = request.form['about']
    #     error = None
    #
    #     if not email:
    #         error = "Email is required."
    #     # elif not about:
    #     #     error = "Say something about you."
    #
    #     if error is None:
    #
    #         return render_template('we-will-write-you-soon.html', user=user)
    #
    #     flash(error)

    return render_template('projects.html', user=user)


@mn.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(mn.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/png')
