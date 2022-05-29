import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, redirect, render_template, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
import flask_login

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# general page controllers
from werkzeug import exceptions
from werkzeug.utils import secure_filename

from controllers.main_page_controller import MainPageController
from controllers.main_menu_controller import MainMenuPageController
from controllers.login_page_controller import LoginPageController
from controllers.registration_page_controller import RegistrationPageController
from controllers.user_manager_page_controller import UserManagerPageController

from controllers.corrections_page_controller import CorrectionsPageController
from controllers.probes_page_controller import ProbesPageController
from controllers.probe_profile_page_controller import ProbeProfileController
from controllers.estimated_values_page_controller import EstimatedValuesPageController
from controllers.age_range_list_page_controller import AgeRangeListPageController
from controllers.results_page_controller import ResultsPageController
from controllers.probationers_page_controller import ProbationersPageController
from controllers.user_profile_page_controller import UserProfilePageController
from controllers.probationer_card_page_controller import ProbationerCardPageController
from controllers.education_main_course_page_controller import EducationMainCoursePageController
from controllers.education_main_course_lesson_page_controller import EducationMainCourseLessonPageController
from controllers.education_list_courses_page_controller import EducationListCoursesPageController
from controllers.education_course_page_controller import EducationCoursePageController
from controllers.education_course_lesson_page_controller import EducationCourseLessonPageController

from error import UserManagerException

import config

sentry_sdk.init(
    dsn="https://216657f6678b4b1bb5136f6ff1a0d8ee@o1211898.ingest.sentry.io/6359936",
    environment=config.ENVIRONMENT,
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

class Config(object):
    DEBUG = config.DEBUG
    LOG_FILE = config.LOG_FILE


if config.DEBUG:
    logging.basicConfig(filename=config.LOG_FILE, level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(name)s %(threadName)s: %(message)s")
else:
    logging.basicConfig(filename=config.LOG_FILE, level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(threadName)s: %(message)s")

handler = RotatingFileHandler(config.LOG_FILE, maxBytes=1048576, backupCount=5)
logger = logging.getLogger()
logger.addHandler(handler)

app = Flask(__name__)
app.secret_key = 'super secret key'
app.debug = config.DEBUG
app.config.from_object(Config())

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """ функция заглушка

    Returns:
        None
    """

    return redirect("main_page")

@app.context_processor
def inject_global_context():
    """инициализация глобальных переменных

    Returns:
        None
    """

    return dict(app_version=config.VERSION, app_name=config.APP_NAME)


@login_manager.user_loader
def load_user(user_id):
    """
    Загрузка данных пользователя

    Args:
        user_id (String): id пользователя

    Returns:

    """    
    login_page_controller = LoginPageController()
    user = login_page_controller.get_user_by_id(user_id)

    return user

@app.route('/debug-sentry')
def trigger_error():
    """служебная процедура для sentry
    """

    division_by_zero = 1 / 0

@app.route("/logout")
@login_required
def logout():
    """
    Страница выхода пользователя из системы

    Returns:

    """

    logout_user()
    return redirect('main_page')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """регистрация нового пользователя

    Returns:
        none
    """

    login_page_controller = RegistrationPageController()
    error_message = ""

    # определяем надо ли создать суперпользователя
    is_create_superuser = False
    if not login_page_controller.is_there_users():
        is_create_superuser = True


    if request.method == 'POST':

        user_login = request.form['login']
        user_name = request.form['user_name']
        user_password = request.form['password']
        user_password2 = request.form['password2']
        user_email = request.form['email']

        try:

            token = login_page_controller.create_user(
                user_login, user_name, user_password, user_password2, user_email, is_create_superuser)
            
            confirm_url = url_for(user_email, token=token, _external=True)
            html = render_template('email_confirmation.html', confirm_url=confirm_url)

            login_page_controller.send_confirmation_email(user_email, html)
            
            return render_template('registration.html', view="registration", _user_created=True,
                                    _error_message="", _create_superuser=False)

        except UserManagerException as e:

            error_message = str(e)

    return render_template('registration.html', view="registration", _user_created=False,
                            _error_message=error_message, _create_superuser=is_create_superuser)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Форма входа пользователя в систему (ввод логина и пароля)

    Returns:

    """

    login_page_controller = LoginPageController()

    # если в системе есть созданный список пользователей, то выполняем процедуру авторизации,
    # если нет, то создаем первого суперпользователя
    if not login_page_controller.is_there_users():
        # пользователей нет, надо создать первого суперпользователя
        return redirect('registration')

    # пользователи есть, проходим процедуру идентификации
    login_error = False

    if request.method == 'POST':

        user_login = request.form['login']
        user_password = request.form['password']

        user = login_page_controller.get_user(user_login, user_password)

        if user is not None:
            if isinstance(user, Exception):
                login_error = user
            else:
                login_user(user)
                return redirect('main_page')

    return render_template('login.html', view="login", _login_error=login_error)


@app.route('/user_manager', methods=['GET', 'POST'])
@login_required
def user_manager():
    """
    Страница управления списков пользователей системы

    Returns:
    """

    page_controller = UserManagerPageController()
    mpc = MainMenuPageController()

    endpoint = "user_manager"

    # страница доступна только администратору
    if not flask_login.current_user.is_admin():
        return redirect("main_page")

    endpoint = request.endpoint

    return render_template('user_manager.html', view="user_manager", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data=page_controller.get_users_list_view(),
                           _is_current_user_admin=flask_login.current_user.is_admin())


@app.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    """
    Страница просмотра и редактирования профиля пользователя
    """

    page_controller = UserProfilePageController()
    mpc = MainMenuPageController()

    endpoint = "user_manager"
    user_id = request.args.get('user_id')

    if user_id is not None and not request.form.get("button"):
        mode = "view"
    else:
        try:
            if request.form["button"] == "save_discharge":
                mode = "discharge"
            else:
                mode = "edit"
        except exceptions.BadRequestKeyError:
            mode = "view"
        pass

    error = None
    settings_user = page_controller.get_settings_user()

    if user_id is None:
        # если пользователь не задан, то открываем страницу в режиме создания нового пользователя
        # страница доступна только администратору
        if not flask_login.current_user.is_admin():
            return redirect("main_page")

        mode = "new"
        user_id = ""
        settings_user = page_controller.get_settings_user()
    else:
        if not flask_login.current_user.is_admin():
            mode = "edit"

    data_begin = page_controller.get_users_profile_view(user_id)
    data = {}
    if isinstance(data_begin, dict):
        active = data_begin['is_active']
    else:
        active = False
    
    error_type = False

    try:
        if request.method == 'POST':
            if request.form["button"] == "add":
                if mode == "new":
                    # добавляем нового пользователя и получаем список с ошибками
                    # если их нет, то получаем пустой список
                    user = {}
                    user["login"] = request.form["login"]
                    user["name"] = request.form["user_name"]
                    user["password"] = request.form["password"]
                    user["password2"] = request.form["password2"]
                    user["email"] = request.form["email"]
                    user["role"] = request.form["role"]
                    user["probationers_number"] = int(request.form["probationers_number"])
                    user["access_time"] = request.form["access_time"]
                    active = True

                    error = page_controller.create_user(user["login"], user["name"], user["password"],
                                                        user["password2"], user["email"], user["role"],
                                                        user["probationers_number"], user["access_time"])

                    if error is None:
                        mode = "view"
                        error = "Пользователь сохранён!"
                        error_type = "Successful"

                    data = user

            elif request.form["button"] == "edit":
                if mode == "view":
                    mode = "edit"

            elif request.form["button"] == "save":
                if mode == "edit":
                    user = {}
                    user["login"] = request.form["login"]
                    user["name"] = request.form["user_name"]
                    user["email"] = request.form["email"]
                    user["role"] = request.form["role"]
                    user["probationers_number"] = int(request.form["probationers_number"])
                    user["access_time"] = request.form["access_time"]
                    user["created_date"] = data_begin["created_date"]
                    user["active"] = data_begin["is_active"]

                    page_controller.change_user(user["login"], user["name"], user["email"], user["role"],
                                                        user["probationers_number"], user["access_time"],
                                                        user["created_date"], user["active"])

                    data = user
                    mode = "view"
                    error = "Изменения сохранены!"
                    error_type = "Successful"

            elif request.form["button"] == "discharge" or request.form["button"] == "save_discharge":
                if mode == "discharge":
                    user = {}
                    user["login"] = request.form["login"]
                    user["password"] = request.form["password"]
                    user["password2"] = request.form["password2"]

                    error = page_controller.discharge_password(user["login"], user["password"], user["password2"])

                    if error is None:
                        mode = "view"

                        error = "Пароль успешно изменен!"
                        error_type = "Successful"

                else:
                    mode = "discharge"

            elif request.form["button"] == "is_active":
                active = page_controller.activation_deactivation(data_begin['login'])
                error_type = "Successful"

                if active:
                    error = "Пользователь успешно разблокирован!"
                else:
                    error = "Пользователь успешно заблокирован!"

                mode = "view"
            
            else:
                return redirect("user_manager")

    except exceptions.BadRequestKeyError:
        mode = "view"

    if data == {}:
        data = data_begin

    return render_template('user_profile.html', view="user_profile", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data=data, _data_begin=data_begin, _settings=settings_user,
                           _is_current_user_admin=flask_login.current_user.is_admin(),
                           _mode=mode, _error=error, _active=active, _error_type=error_type)


@app.route('/main_page', methods=['GET', 'POST'])
@login_required
def main_page():
    """
    Просмотр и редактирование собственнного профиля

    Returns:
        
    """    

    page_controller = MainPageController()
    mpc = MainMenuPageController()

    endpoint = request.endpoint

    return render_template('main_page.html', view="main_page", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data=page_controller.get_actions(), _user=page_controller.get_current_user())


@app.route('/empty_function', methods=['GET', 'POST'])
@login_required
def empty_function():
    """
    Пустая функция-заглушка

    Returns:
        
    """

    page_controller = None
    mpc = MainMenuPageController()

    endpoint = request.endpoint

    return render_template('index.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data="")

@app.route('/education_main_course/lesson', methods=['GET', 'POST'])
@login_required
def education_main_course_lesson():

    page_controller = EducationMainCourseLessonPageController()
    mpc = MainMenuPageController()

    endpoint = request.endpoint

    id_lesson = request.args.get("id_lesson")
    id_video = request.args.get("id_video")
    if id_video is None:
        id_video = 1

    data = page_controller.get_lesson(int(id_lesson), int(id_video))

    return render_template('education_courses_lesson.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data=data)


@app.route('/education_main_courses', methods=['GET', 'POST'])
@login_required
def education_main_courses():
    """
    Пустая функция-заглушка

    Returns:
        
    """

    return redirect("/education_course?id_course=1")

@app.route('/education_list_courses', methods=['GET', 'POST'])
@login_required
def education_list_courses():

    page_controller = EducationListCoursesPageController()
    mpc = MainMenuPageController()

    data = page_controller.get_courses()

    endpoint = request.endpoint

    return render_template('education_list_courses.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _data=data)

@app.route('/education_course', methods=['GET', 'POST'])
@login_required
def education_course():

    page_controller = EducationCoursePageController()
    mpc = MainMenuPageController()

    id_course = request.args.get("id_course")

    if id_course is not None:
        data = page_controller.get_course(id_course)
    else:
        data = None

    endpoint = request.endpoint


    return render_template('education_course.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _data=data)

@app.route('/education_course/lesson', methods=['GET', 'POST'])
@login_required
def education_course_lesson():

    page_controller = EducationCourseLessonPageController()
    mpc = MainMenuPageController()

    endpoint = request.endpoint

    id_course = request.args.get("id_course")
    id_lesson = int(request.args.get("id_lesson"))
    id_video = request.args.get("id_video")
    id_room_chat = request.args.get("id_chat")
    user = page_controller.get_current_user()
    user_list = None
    if id_room_chat is None:
        if user["role"] != "superuser":
            id_room_chat = page_controller.room_chat_entry(id_lesson, id_course)["id"]
            return redirect(f"/education_course/lesson?id_course={id_course}&id_lesson={id_lesson}&id_video={id_video}&id_chat={id_room_chat}")

    if id_video is None:
        id_video = 1

    if user["role"] == "superuser":
        user_list = page_controller.get_user_list()

    if request.method == "POST":
        if request.form.get("send"):
            text = request.form.get("text")
            files = request.files.getlist("files")
            page_controller.add_message({"text": text, "files": files}, id_room_chat)
            # room_chat = page_controller.room_chat_entry(_id_room_chat=id_room_chat)
        else:
            id_room_chat = page_controller.room_chat_entry(id_lesson, id_course, request.form.get("user"))["id"]
            return redirect(
                f"/education_course/lesson?id_course={id_course}&id_lesson={id_lesson}&id_video={id_video}&id_chat={id_room_chat}")

    data = page_controller.get_lesson(id_lesson, int(id_course), int(id_video))
    room_chat = page_controller.room_chat_entry(_id_room_chat=id_room_chat)
    # if user_role != "superuser":
    #     room_chat = page_controller.room_chat_entry(id_lesson, id_course)

    return render_template('education_courses_lesson.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data=data, _room_chat=room_chat, _user_list=user_list, _user=user)

@app.route('/education_home_tasks', methods=['GET', 'POST'])
@login_required
def education_home_tasks():
    """
    Пустая функция-заглушка

    Returns:
        
    """

    page_controller = None
    mpc = MainMenuPageController()

    endpoint = request.endpoint

    return render_template('index.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data="")

@app.route('/corrections', methods=['GET', 'POST'])
@login_required
def corrections():
    """
    Просмотр выполнение нейро-психологических коррекций

    Returns:
        
    """    

    page_controller = CorrectionsPageController()
    mpc = MainMenuPageController()

    endpoint = request.endpoint

    return render_template('corrections.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data=page_controller.get_data())

@app.route('/probes', methods=['GET', 'POST'])
@login_required
def probes():
    """
    Просмотр проведение нейро-психологических проб

    Returns:
        
    """    

    page_controller = ProbesPageController()
    mpc = MainMenuPageController()

    endpoint = request.endpoint

    return render_template('protocols.html', view="probes", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data=page_controller.get_probes(), _is_probationer=page_controller.is_probationers())

@app.route('/probe_profile', methods=['GET', 'POST'])
@login_required
def probe_profile():

    page_controller = ProbeProfileController()
    mpc = MainMenuPageController()

    endpoint = "probes"
    probationer_id = request.args.get('probationer_id')

    data = {}
    test_list = []
    probationers = []
    probe_id = request.args.get("probe_id")
    protocol = ""

    if probationer_id is None:
        probationers.append({"name_probationer": "Выберите тестируемого"})
        probationers.extend(page_controller.get_probationers())
        mode = "selection_probationer"
    else:
        test_id = int(request.args.get("test_id"))
        data = page_controller.get_protocol(test_id, int(probe_id))
        if data is not None:
            protocol = data["protocol_status"]
        else:
            protocol = None
        mode = "add_value_tests"
        test_list = page_controller.get_tests_list()

    if request.method == "POST":
        if mode == "selection_probationer":
            name_probationer = request.form["probationer"]
            probationer = [i for i in probationers if i["name_probationer"] == name_probationer][0]
            probationer_id = probationer["probationer_id"]
            date_of_birth = probationer["date_of_birth"]

            probe_id = page_controller.add_probe(name_probationer, probationer_id, date_of_birth)
            return redirect("probe_profile?probationer_id={probationer_id}&probe_id={probe_id}&test_id=1".format(
                probationer_id=probationer_id,
                probe_id=probe_id
            ))

        elif mode == "add_value_tests":
            probe_id = request.args.get("probe_id")
            grades = [{"id": key, "grade": value} for key, value in request.form.items() if key.isdigit() or ("_" in key)]
            page_controller.add_grades_in_probe(grades, int(probe_id))

            if request.form.get("button") == "draft" or request.form.get("button") == "end":
                protocol_status = request.form["button"]
                page_controller.add_grades_in_probe(grades, int(probe_id), protocol_status)

                return redirect("probes")

            elif request.form["action"]:
                page_controller.add_grades_in_probe(grades, int(probe_id))
                next_test_id = int(request.form["action"])

                return redirect("probe_profile?probationer_id={probationer_id}&probe_id={probe_id}&test_id={test_id}".format(
                    probationer_id=probationer_id,
                    probe_id=probe_id,
                    test_id=next_test_id
                ))

    return render_template('probe_profile.html', view="probe_profile", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _probationers_list=probationers, _data=data,
                           _mode=mode, _probes=test_list, _protocol=protocol)

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    """
    Просмотр результатов тестирования

    Returns:
        
    """    

    page_controller = ResultsPageController()
    mpc = MainMenuPageController()

    endpoint = request.endpoint

    return render_template('results.html', view="results", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data=page_controller.get_data())

@app.route('/probationers', methods=['GET', 'POST'])
@login_required
def probationers():
    """
    Просмотр списка испытуемых

    Returns:
        
    """    

    page_controller = ProbationersPageController()
    mpc = MainMenuPageController()

    global attempt
    attempt = False

    endpoint = request.endpoint

    return render_template('probationers.html', view="probationers", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data=page_controller.get_probationers_list_view(),
                           _is_current_user_admin=flask_login.current_user.is_admin())

@app.route('/probationer_card', methods=['GET', 'POST'])
@login_required
def probationer_card():
    """
        Страница просмотра, редактирования и добавления карточки испытуемого
    """

    page_controller = ProbationerCardPageController()
    mpc = MainMenuPageController()
    endpoint = "probationers"

    probationer_id = request.args.get('probationer_id')
    global attempt
    error = None
    error_type = None

    if not (attempt and probationer_id is not None):
        mode = "view"
    else:
        mode = "edit"

    if probationer_id is None:
        mode = "new"
        probationer_id = ""

    user_id = flask_login.current_user.user_id
    user_login = UserProfilePageController().get_users_profile_view(user_id).login

    data_begin = page_controller.get_probationer_card_view(probationer_id)
    data = {}

    try:
        if request.method == 'POST':
            if request.form["button"] == "add_save_edit":
                if mode == "new":
                    # добавляем нового пользователя и получаем список с ошибками
                    # если их нет, то получаем пустой список
                    attempt = True
                    probationer = {}
                    probationer["name_probationer"] = request.form["name_probationer"]
                    probationer["date_of_birth"] = request.form["date_of_birth"]
                    probationer["name_parent"] = request.form["name_parent"]
                    probationer["educational_institution"] = request.form["educational_institution"]
                    probationer["contacts"] = request.form["contacts"]
                    probationer["diagnoses"] = request.form["diagnoses"]
                    probationer["reasons_for_contact"] = request.form["reasons_for_contact"]

                    error = page_controller.create_probationers(user_login, probationer["name_probationer"],
                                                                probationer["date_of_birth"], probationer["name_parent"],
                                                                probationer["educational_institution"],
                                                                probationer["contacts"], probationer["diagnoses"],
                                                                probationer["reasons_for_contact"])

                    if error is None:
                        mode = "view"
                        error = "Испытуемый сохранён!"
                        error_type = "Successful"
                        attempt = False

                    data = probationer

                elif mode == "view":

                    mode = "edit"
                    attempt = True

                elif mode == "edit":

                    probationer = {}

                    probationer["name_probationer"] = request.form["name_probationer"]
                    probationer["date_of_birth"] = request.form["date_of_birth"]
                    probationer["name_parent"] = request.form["name_parent"]
                    probationer["educational_institution"] = request.form["educational_institution"]
                    probationer["contacts"] = request.form["contacts"]
                    probationer["diagnoses"] = request.form["diagnoses"]
                    probationer["reasons_for_contact"] = request.form["reasons_for_contact"]

                    page_controller.change_probationer(probationer_id, probationer["name_probationer"],
                                                        probationer["date_of_birth"], probationer["name_parent"],
                                                        probationer["educational_institution"],
                                                        probationer["contacts"],
                                                       probationer["diagnoses"], probationer["reasons_for_contact"])

                    data = probationer
                    mode = "view"
                    attempt = False
                    error = "Изменения сохранены!"
                    error_type = "Successful"

    except exceptions.BadRequestKeyError:

        mode = "view"
        attempt = False

    if data == {}:
        data = data_begin

    return render_template('probationer_card.html', view="probationer_card", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _data=data,
                           _mode=mode, _data_begin=data_begin, _error=error, _error_type=error_type, _attempt=attempt)

@app.route('/settings/age_range_list', methods=['GET', 'POST'])
@login_required
def age_range_list():
    """
    Генерация страницы просмотра списка диапазонов возрастов

    Returns:

    """

    page_controller = AgeRangeListPageController()
    mpc = MainMenuPageController()

    endpoint = request.endpoint

    return render_template('age_range_list.html', view="age_range_list", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _ranges_age=page_controller.get_age_ranges(),
                           _is_current_user_admin=flask_login.current_user.is_admin(), _endpoint=endpoint)

@app.route('/settings/estimated_values', methods=['GET', 'POST'])
@login_required
def estimated_values():
    """
    Генерация страницы редактирования оценочных значений

    Returns:

    """
    page_controller = EstimatedValuesPageController()
    mpc = MainMenuPageController()

    endpoint = request.endpoint
    id_file_name = request.args.get("id")

    if id_file_name is not None:
        data = page_controller.get_assessments(int(id_file_name))
    else:
        return redirect("/settings/estimated_values?id=1")

    if request.method == "POST":
        id_file_name = int(request.form["action"])

        if request.form.get("save") is not None:
            criteria = []

            for i in range(1, 214):
                criteria.append(request.form["{}_grade".format(i)])

            page_controller.overwrite(id_file_name, criteria)
            data = page_controller.get_assessments(id_file_name)
        else:
            return redirect("/settings/estimated_values?id={id}".format(id=id_file_name))

    return render_template('estimated_values.html', view="estimated_values", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data=data, _ranges_age=page_controller.get_age_ranges(), _id_file_name=int(id_file_name),
                           _is_current_user_admin=flask_login.current_user.is_admin(), _endpoint=endpoint)

@app.errorhandler(404)
@login_required
def not_found(e):
    """
    Форма обработки ошибки 404

    Args:
        e ([Exeprion]): ошибка

    Returns:

    """    

    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
