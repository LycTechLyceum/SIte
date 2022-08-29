from flask import Blueprint, render_template, request, flash, session, url_for, redirect
import requests
adm = Blueprint('admin', __name__)
URL = 'https://lyctech-db-test.herokuapp.com/api/'  # часть api для доступа к хероку


@adm.route('/admin', methods=('GET', 'POST'))  # страница для входа на страницу админа
def admin_login():
    if 'login' not in session:  # if LOGIN in session - login it without questions
        return redirect(url_for('main_pages.login'))
    if request.method == 'POST':
        token = request.form['token']
        print(token)
        error = None
        if not token:
            error = 'Token is required.'

        if error is None:
            check_token = requests.get(URL + 'check-token', json={'login': session['login'], 'token': token}).json()
            print(session)
            print(check_token)
            if check_token['error'] == False:  # проверяем токен админа
                print(1)
                return redirect(url_for('admin.admin_main_page'))
            else:
                print(2)
                return redirect(url_for('admin.admin_login'))
        flash(error)

    return render_template('admin-login.html')  # если токен не совпал, то просим еще раз ввести токен


@adm.route('/admin-main')
def admin_main_page():  # главная страница с кнопками для перехода на страницу со всей инфой
    return render_template("admin-main-page.html")


@adm.route('/all-organizations')
def all_organizations():  # все организации
    organizations_req = requests.get(URL + 'organizations').json()  # получаем список всех организации
    # print(organizations_req)

    organizations = []
    for org_number in organizations_req:  # делаем список всех организаций удобнее для работы в html
        organizations.append(organizations_req[str(org_number)])

    return render_template("all_org.html", organizations=organizations)


@adm.route('/<string:name>/organisation-page', methods=('GET', 'POST'))  # страница организации
def org_page(name):
    # print(name)
    organisation_info = requests.get(URL + 'organization', json={"name": str(name)}).json()  # получаем инфо об организации
    # print(organisation_info)
    return render_template('org_page.html', organisation_info=organisation_info)


@adm.route('/all-projects')  # станица всех проектов
def all_projects():
    # add_event = requests.post('https://db-proglyc-hse.herokuapp.com/api/get-events/api/post-event',
    #                           json={"event_name": "event_name", "login_cur": "login", "login_cus": "login",
    #                                 "org_name": "org1"})
    # print(add_event)
    projects = requests.get(URL + 'events').json()
    # print(projects)
    # projects = {1: "project1"}
    return render_template("all_projects.html", projects=projects)


@adm.route('/<string:id>/project-page', methods=('GET', 'POST'))  # страница проекта
def project_page(id):  # страница одного проекта по ID
    # print(id)
    project_info = requests.get(URL + 'event', json={"id": id}).json()  # получаем инфо о проекте по id
    # project_info = {"id": id, "name": "project1", "date": "10.03.2022",
    #                         "curator": {"id": 1, "name": "Tim"},
    #                         "customer": {"id": 1, "name": "Artem"},
    #                         "organization": {"id": 1, "name": "имя организации 1.1"},
    #                         "progers": [{"id": 1, "name": "Tim"}], "visitors": [{"id": 1, "name": "Tim"}]}
    return render_template('project_page.html', project_info=project_info)


@adm.route('/all-users')  # страница всех пользователей
def all_users():
    users = requests.get(URL + 'users').json()
    # print(users)
    return render_template("all_users.html", users=users)


@adm.route('/<int:id>/user-page', methods=('GET', 'POST'))  # страница пользователя
def user_page(id):
    # print(id)
    user = requests.get(URL + 'user', json={"id": id}).json()  # получаем инфо о пользователе по id
    # user = {"id": 1, "name": "Tim", "surname": "Smirnov", "grade": "11и4",
    #                 "login": "login", "password": "12345", "position": {"id": 1, "name": "master"},
    #                 "date": "10.03.2005"}
    # print(user)
    return render_template('user_page.html', user=user)


@adm.route('/all-pos')  # страница всех позиций (глава, куратор, прогаммист, пользователь)
def all_pos():
    positions = requests.get(URL + 'positions').json()
    # print(positions)
    return render_template("all_pos.html", positions=positions)


@adm.route('/<int:id>/pos-page', methods=('GET', 'POST'))  # страница позиции
def pos_page(id):
    # print(id)
    position_info = requests.get(URL + 'position', json={"id": int(id)}).json()  # получаем инфо о позиции по id
    # print(position_info)
    # position_info = {"id": 1, "name": "Master", "participants": [{"id": 1, "name": "Tim", "surname": "Smirnov"}]}
    return render_template('pos_page.html', pos_info=position_info)


@adm.route('/all-practices')  # все практикумы
def all_practices():
    practices = requests.get(URL + 'practices').json()
    # print(practices)
    return render_template("all_practices.html", practices=practices)


@adm.route('/<int:id>/practice-page', methods=('GET', 'POST'))  # страница практикума по ID
def practice_page(id):
    practice = requests.get(URL + 'practice', json={'id': id}).json()
    # practice = {"id": 1, "name": "First", "organizer": {"id": 1, "name": "Tim", "surname": "Smirnov"},
    #             "visitors": [{"id": 1, "name": "Tim", "surname": "Smirnov"}]}
    # print(practice)
    return render_template('prac_page.html', practice=practice)


@adm.route('/all-programmers')  # страница всех программистов
def all_programmers():
    programmers = requests.get(URL + 'progers').json()
    # print(programmers)
    # programmers = {1: {"id": 1, "name": "Tim", "surname": "Smirnov",
    #                 "events": [{"id": 1, "name": "project1"}]}}
    return render_template("all_programmers.html", programmers=programmers)


# @adm.route('/<int:id>/proger-page', methods=('GET', 'POST'))  # страница программиста
# def proger_page(id):
#     # print(id)
#     # proger_info = requests.get('https://db-proglyc-hse.herokuapp.com/api/post-proger',
#     #                                  json={"id": int(id)}).json()  # получаем инфо о программисте по id
#     programmer = {}  # пока что нету ничего, Матвей работает над этим
#     return render_template('proger_page.html')


@adm.route('/all-visitors')  # встраница всех посетителей проектов (приодит инфа с других сайтов)
def all_visitors():
    visitors = requests.get(URL + 'visitors').json()
    # print(visitors)
    #
    # visitors = []
    # for visitor in visitors_req:
    #     visitors.append([visitor, visitors_req[visitor]])
    # visitors = {1: {"id": 1, "name": "Tim", "surname": "Smirnov",
    #                 "events": [{"id": 1, "name": "project1"}]}}
    return render_template("all_visitors.html", visitors=visitors)


# @adm.route('/<int:id>/visitor-page', methods=('GET', 'POST'))  # страница посетителя наших продуктов
# def visitor_page(id):
#     # print(id)
#     # visitor_info = requests.get('https://db-proglyc-hse.herokuapp.com/api/post-visitor',
#     #                                  json={"id": int(id)}).json()  # получаем инфо о программисте по id
#     # print(visitor_info)
#     return render_template('visitor_page.html')


@adm.route('/all-practices-boys')  # траница посетителей практикумов
def all_practices_boys():
    practices_boys = requests.get(URL + 'visitor-practice').json()
    # practices_boys = {1: {"id": 1, "name": "Tim", "surname": "Smirnov",
    #                     "practice": [{"id": 1, "name": "First"}]}}
    return render_template("all_practices_boys.html", practices_boys=practices_boys)


@adm.route('/all-masters')  # страница всех глав
def all_masters():
    masters = requests.get(URL + 'leaders').json()
    # masters = {1: {"id": 1, "name": "Tim", "surname": "Smirnov", "email": "ts5310m@gmail.com"}}
    return render_template("all_masters.html", masters=masters)


@adm.route('/all-customers')  # страница всех заказчиков
def all_customers():
    customers = requests.get(URL + 'customers').json()
    # customers = {1: {"id": 1, "name": "Tim", "surname": "Surname",
    #             "events": [{"id": 1, "name": "project1"}]}}
    return render_template("all_customers.html", customers=customers)


@adm.route('/all-curators')  # траница всех кураторов
def all_curators():
    curators = requests.get(URL + 'curators').json()
    # curators = {1: {"id": 1, "name": "Tim", "surname": "Surname",
    #             "events": [{"id": 1, "name": "project1"}]}}
    return render_template("all_curators.html", curators=curators)
