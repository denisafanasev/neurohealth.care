import logging
from logging.handlers import RotatingFileHandler

from flask_babel import Babel, gettext
from flask import Flask, request, redirect, render_template, send_file, abort, session, Blueprint, g, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
import flask_login

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# general page controllers
from werkzeug import exceptions

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
from controllers.education_list_courses_page_controller import EducationListCoursesPageController
from controllers.education_course_page_controller import EducationCoursePageController
from controllers.education_course_lesson_page_controller import EducationCourseLessonPageController
from controllers.download_page_controller import DownloadPageController
from controllers.education_home_tasks_page_controller import EducationHomeTasksPageController
from controllers.education_home_task_card_page_controller import EducationHomeworkCardPageController
from controllers.education_streams_page_controller import EducationStreamsPageController
from controllers.education_stream_page_controller import EducationStreamPageController
from controllers.education_program_subscription_page_controller import EducationProgramSubscriptionPageController
from controllers.maintenance_page_controller import MaintenancePageController
from controllers.user_actions_page_controller import UserActionsPageController

from error import UserManagerException

import config

sentry_sdk.init(
    dsn=config.sentry_dsn(),
    environment=config.ENVIRONMENT,
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

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

login_manager = LoginManager()
login_manager.login_view = "multilingual.login"
login_manager.init_app(app)


def get_locale():
    # if a user is logged in, use the locale from the user settings

    languages = [language['lang_code'] for language in config.LANGUAGES]
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(languages)
    return g.lang_code


multilingual = Blueprint('multilingual', __name__, template_folder='templates', url_prefix='/<lang_code>')


@multilingual.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@multilingual.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@multilingual.before_request
def before_request():
    """

    """

    languages = [language['lang_code'] for language in config.LANGUAGES]
    if g.lang_code not in languages:
        adapter = app.url_map.bind('')
        try:
            endpoint, args = adapter.match(
                '/ru' + request.full_path.rstrip('/ ?'))
            return redirect(url_for(endpoint, **args), 301)
        except:
            abort(404)

    dfl = request.url_rule.defaults
    if 'lang_code' in dfl:
        if dfl['lang_code'] != request.full_path.split('/')[1]:
            abort(404)


@app.route('/', methods=['GET', 'POST'])
@multilingual.route('/', methods=['GET', 'POST'])
@multilingual.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """ функция заглушка

    Returns:
        None
    """

    return redirect(url_for("multilingual.main_page"))


@multilingual.context_processor
def inject_global_context():
    """
    инициализирует глобальные переменные

    Returns:
        None
    """

    ga_id = config.ga_id()
    cdp_id = config.cdp_id()
    app_support_channel = config.app_support_channel()

    return dict(app_version=config.VERSION,
                app_name=config.APP_NAME,
                GA_TRACKING_ID=ga_id,
                APP_SUPPORT_CHANNEL=app_support_channel,
                CDP_TRACKING_ID=cdp_id)


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


@multilingual.route('/debug-sentry')
def trigger_error():
    """
    служебная процедура для sentry
    """

    division_by_zero = 1 / 0


@multilingual.route("/logout")
@login_required
def logout():
    """
    Страница выхода пользователя из системы

    Returns:

    """

    logout_user()
    return redirect(url_for('multilingual.main_page'))


@multilingual.route('/registration', methods=['GET', 'POST'])
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

            # TODO: доделать подтверждение почты

            # confirm_url = url_for(user_email, token=token, _external=True)
            # html = render_template('email_confirmation.html', confirm_url=confirm_url)

            # login_page_controller.send_confirmation_email(user_email, html)

            return render_template('registration.html', view="registration", _user_created=True,
                                   _error_message="", _create_superuser=False)

        except UserManagerException as e:

            error_message = str(e)

    return render_template('registration.html', view="registration", _user_created=False,
                           _error_message=error_message, _create_superuser=is_create_superuser)


@multilingual.route('/login', methods=['GET', 'POST'])
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
        return redirect(url_for('multilingual.registration'))

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
                return redirect(url_for('multilingual.main_page'))

    return render_template('login.html', view="login", _login_error=login_error)


@multilingual.route('/user_manager', methods=['GET', 'POST'])
@login_required
def user_manager():
    """
    Страница управления списков пользователей системы

    Returns:
    """

    page_controller = UserManagerPageController()
    current_user_id = flask_login.current_user.user_id
    mpc = MainMenuPageController(current_user_id)

    # страница доступна только администратору
    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.main_page"))

    endpoint = request.endpoint
    users_list = page_controller.get_users_list_view(current_user_id)

    error = None
    error_type = None
    num_page = 0

    return render_template('user_manager.html', view="user_manager", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _users_list=users_list, _is_current_user_admin=flask_login.current_user.is_admin(),
                           _error=error, _error_type=error_type, _num_page=num_page, _languages=config.LANGUAGES,
                           _lang_code=get_locale())


@multilingual.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    """
    Страница просмотра и редактирования профиля пользователя
    """

    page_controller = UserProfilePageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    endpoint = "user_manager"
    user_id = request.args.get('user_id')
    current_user_id = flask_login.current_user.user_id

    if user_id is not None and not request.form.get("button"):
        mode = "view"
    else:
        mode = "edit"

    message_error = session.get('message_error')
    status_code = session.get('status_code')
    if status_code is not None:
        session.pop('status_code')

    if message_error is not None:
        session.pop('message_error')

    settings_user = page_controller.get_settings_user()
    # страница доступна только администратору
    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.main_page"))

    if user_id is None:
        mode = "new"
        user_id = ""
        settings_user = page_controller.get_settings_user()
    else:
        user_id = int(user_id)

    data = page_controller.get_users_profile_view(user_id)
    education_streams_list = page_controller.get_education_streams_list(user_id, data['role'])
    data_edit = {}
    active_tab = 'user_profile'

    try:
        if request.method == 'POST':
            if request.form.get("button") == "add":
                if mode == "new":
                    # добавляем нового пользователя и получаем список с ошибками
                    # если их нет, то получаем id пользователя
                    user = {}
                    user["login"] = request.form["login"]
                    user["name"] = request.form["user_name"]
                    user["password"] = request.form["password"]
                    user["password2"] = request.form["password2"]
                    user["email"] = request.form["email"]
                    user["role"] = request.form["role"]
                    user["probationers_number"] = int(request.form["probationers_number"])
                    user['active'] = True

                    message_error = page_controller.create_user(user["login"], user["name"], user["password"],
                                                                user["password2"], user["email"], user["role"],
                                                                user["probationers_number"], current_user_id)
                    if isinstance(message_error, int):
                        session['message_error'] = "Пользователь сохранён!"
                        session['status_code'] = "Successful"

                        return redirect(url_for('multilingual.user_profile', user_id=message_error))
                    else:
                        status_code = 'Error'

                    data_edit = user

            elif request.form.get("button") == "edit":
                if mode == "view":
                    mode = "edit"

            elif request.form.get("button") == "save":
                if mode == "edit":
                    user = {}
                    user["login"] = data['login']
                    user["name"] = request.form["user_name"]
                    user["email"] = request.form["email"]
                    user["role"] = request.form["role"]
                    user["probationers_number"] = int(request.form["probationers_number"])
                    user["created_date"] = data["created_date"]
                    user['education_module_expiration_date'] = data["education_module_expiration_date"]
                    user['active'] = request.form.get('is_active')
                    if user['active'] is not None:
                        user['active'] = True
                    else:
                        user['active'] = False

                    message_error = page_controller.chenge_user(user_id, user["login"], user["name"], user["email"],
                                                                user["role"],
                                                                user["probationers_number"], user["created_date"],
                                                                user['education_module_expiration_date'],
                                                                user['active'], current_user_id)
                    if message_error is None:
                        session['message_error'] = "Изменения сохранены!"
                        session['status_code'] = "Successful"

                        return redirect(url_for('multilingual.user_profile', user_id=user_id))
                    else:
                        status_code = 'Error'

                    data_edit = user

            elif request.form.get("button") == "reset":
                user = {}
                user["password"] = request.form["password"]
                user["password2"] = request.form["password2"]

                session['message_error'], session['status_code'] = page_controller.chenge_password(user_id,
                                                                                                   user["password"],
                                                                                                   user["password2"],
                                                                                                   current_user_id)
                if session['status_code'] == 'Successful':
                    return redirect(url_for('multilingual.user_profile', user_id=user_id))

                else:
                    data_edit = data.copy()
                    data_edit['password'] = user["password"]
                    data_edit['password2'] = user['password2']
                    message_error = session.pop('message_error')
                    status_code = session.pop('status_code')

                mode = 'view'

            elif request.form.get("button") == "extension":
                reference_point = request.form["reference_point"]
                period = request.form["period"]
                session['message_error'] = page_controller.access_extension(int(period), reference_point, user_id,
                                                                            current_user_id)
                session['status_code'] = "Successful"

                return redirect(url_for('multilingual.user_profile', user_id=user_id))

            elif request.form.get("is_active"):
                if mode == 'view':
                    is_active = request.form.get("is_active")
                    if is_active == "true":
                        session['message_error'] = page_controller.activation(user_id, current_user_id)
                        data['active'] = True
                        session['status_code'] = 'Successful'

                    elif is_active == 'false':
                        session['message_error'] = page_controller.deactivation(user_id, current_user_id)
                        data['active'] = False
                        session['status_code'] = 'Successful'

                    return redirect(url_for('multilingual.user_profile', user_id=user_id))
            else:
                return redirect(url_for("multilingual.user_manager"))

    except exceptions.BadRequestKeyError:
        mode = "view"

    if data_edit == {}:
        data_edit = data

    return render_template('user_profile.html', view="user_profile", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data_edit=data_edit, _data=data, _settings=settings_user,
                           _is_current_user_admin=flask_login.current_user.is_admin(), _user_id=user_id,
                           _mode=mode, _message_error=message_error, _status_code=status_code,
                           _education_streams_list=education_streams_list, _active_tab=active_tab,
                           _lang_code=get_locale(), _languages=config.LANGUAGES)


@multilingual.route('/user_actions', methods=['GET', 'POST'])
@login_required
def user_actions():
    """
    Просмотр действий пользователя

    Returns:
        None
    """

    page_controller = UserActionsPageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    endpoint = "user_manager"
    active_tab = 'user_actions'
    user_id = request.args.get('user_id')
    current_user_id = flask_login.current_user.user_id

    if not flask_login.current_user.is_admin():
        return redirect(url_for('multilingual.main_page'))

    mode = 'actions'
    if user_id is not None:
        user_id = int(user_id)

    data = page_controller.get_actions(user_id)

    return render_template('user_actions.html', view="user_profile", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data=data, _is_current_user_admin=flask_login.current_user.is_admin(),
                           _user_id=user_id, _mode=mode, _active_tab=active_tab, _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/main_page', methods=['GET', 'POST'])
@login_required
def main_page():
    """
    Просмотр и редактирование собственнного профиля

    Returns:
        
    """

    page_controller = MainPageController()
    user_id = flask_login.current_user.user_id
    mpc = MainMenuPageController(user_id)

    user = page_controller.get_user_view_by_user_id(user_id)
    endpoint = request.endpoint
    message_error = session.get('message_error')
    status_code = session.get('status_code')
    if message_error is not None:
        session.pop('message_error')

    if status_code is not None:
        session.pop('status_code')

    password = ''
    password2 = ''
    education_streams_list = page_controller.get_education_streams(user_id)
    progress_list = page_controller.get_progress_users(user_id)

    if request.method == "POST":
        if request.form.get("button") == "reset":
            password = request.form['password']
            password2 = request.form["password2"]
            current_password = request.form['current_password']

            message_error = page_controller.chenge_password(user['user_id'], password, password2, current_password)
            if message_error is None:
                session['message_error'] = gettext("Пароль успешно изменен!")
                session['status_code'] = "Successful"
            else:
                session['message_error'] = str(message_error)
                session['status_code'] = "Error"

            return redirect(url_for('multilingual.main_page'))

    return render_template('main_page.html', view="main_page", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data=page_controller.get_actions(user["user_id"]), _user=user, _message_error=message_error,
                           _status_code=status_code, _password=password, _password2=password2,
                           _education_streams_list=education_streams_list, _lang_code=get_locale(),
                           _languages=config.LANGUAGES, _progress_list=progress_list)


@multilingual.route('/empty_function', methods=['GET', 'POST'])
@login_required
def empty_function():
    """
    Пустая функция-заглушка

    Returns:
        
    """

    page_controller = None
    user_id = flask_login.current_user.user_id
    mpc = MainMenuPageController(user_id)

    endpoint = request.endpoint

    return render_template('index.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _data="")


@multilingual.route('/education_program_subscription', methods=['GET', 'POST'])
@login_required
def education_program_subscription():
    """
    Страница прайс листа и подписки на платформу

    Returns:

    """

    endpoint = 'education_list_courses'
    page_controller = EducationProgramSubscriptionPageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    endpoint = 'education_list_courses'
    user_id = flask_login.current_user.user_id

    _data = page_controller.get_page_data(1)

    return render_template('education_program_subscription.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _data=_data, _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/evolution_centre_dummy', methods=['GET', 'POST'])
@login_required
def evolution_centre_dummy():
    """
    Страница заглушка для разделов, которые еще не готовы

    Returns:
        
    """

    mpc = MainMenuPageController(flask_login.current_user.user_id)

    endpoint = request.endpoint
    user_id = flask_login.current_user.user_id

    return render_template('evolution_centre_dummy.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data="", _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


# @app.route('/education_list_courses', methods=['GET', 'POST'])
@multilingual.route('/education_list_courses')
@login_required
def education_list_courses():
    """
    Просмотр списка курсов

    Returns:

    """
    page_controller = EducationListCoursesPageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    endpoint = request.endpoint
    user_id = flask_login.current_user.user_id

    data = page_controller.get_courses()
    user = page_controller.get_user_view_by_id(user_id)
    user_education_progress = page_controller.get_user_education_progress(user_id)

    return render_template('education_list_courses.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _data=data, _user=user,
                           _user_education_progress=user_education_progress, full_path=request.full_path,
                           _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/education_course', methods=['GET', 'POST'])
@login_required
def education_course():
    """
    Просмотр списка модулей и уроков курса

    Returns:

    """
    page_controller = EducationCoursePageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    endpoint = 'education_list_courses'

    course_id = request.args.get("id_course")
    user_id = flask_login.current_user.user_id  # берем id пользователя, который находится в системе

    if course_id is not None:
        user = page_controller.get_user_view_for_course_by_id(user_id, course_id)
        course = page_controller.get_course_by_id(course_id)
        data = page_controller.get_course_modules_list(int(course_id), user_id)
    else:
        return redirect(url_for("multilingual.education_list_courses"))

    if request.method == "POST":
        # если пользователь переходит на страницу урока, то записываем данное действие в базу данных
        if request.form.get("button"):
            id_lesson = int(request.form['button'])
            return page_controller.redirect_to_lesson(id_lesson, user_id)

    return render_template('education_course.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _data=data,
                           _user=user, _course_type=course.get('type'), _course_name=course.get('name'), _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/education_course/lesson', methods=['GET', 'POST'])
@login_required
def education_course_lesson():
    """
    Просмотр урока, сдача домашней работы и чат для ощения с кураторами

    Returns:

    """
    page_controller = EducationCourseLessonPageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    endpoint = 'education_list_courses'
    user_id = flask_login.current_user.user_id

    try:
        id_lesson = int(request.args.get("id_lesson"))
    except (ValueError, TypeError) as e:
        abort(404)

    try:
        id_video = int(request.args.get("id_video"))
    except (ValueError, TypeError) as e:
        return redirect(url_for('multilingual.education_course_lesson', id_video=1, id_lesson=id_lesson))

    user = page_controller.get_user_view_by_id(user_id)
    data = page_controller.get_lesson(user_id, id_lesson, id_video)
    homework = None
    homework_chat = None
    course = None
    neighboring_lessons = None
    error_message = session.get('error_message')
    status_code = session.get('status_code')
    if session.get('error_message') is not None:
        session.pop('error_message')

    if session.get('status_code') is not None:
        session.pop('status_code')

    if data is not None:
        course = page_controller.get_course_by_id(data['id_course'])

        neighboring_lessons = page_controller.get_neighboring_lessons(user_id, id_lesson, data['id_course'])
        if not data['available']:
            return redirect(url_for('multilingual.education_program_subscription'))

    if id_video is None:
        id_video = 1

    if request.method == "POST":
        # сохраняем новое сообщение
        if request.form.get("send"):
            text = request.form.get("text")
            session['error_message'] = page_controller.add_message({"text": text, "id_user": user_id}, id_lesson)
            if session.get('error_message') is not None:
                session['status_code'] = 'Error'

        # сохраняем домашнюю работу
        elif request.form.get("button") == "homework":
            files = request.files.getlist("files")
            text = request.form.get("text_homework")
            session['error_message'] = page_controller.save_homework(files, user_id, text, id_lesson)
            if session.get('error_message') is not None:
                session['status_code'] = 'Error'

        return redirect(url_for('multilingual.education_course_lesson', id_video=1, id_lesson=id_lesson))

    if data is not None:
        if data['available']:
            homework = page_controller.get_last_homework(id_lesson, user_id)
            homework_chat = page_controller.get_homework_chat(id_lesson, user_id)

    return render_template('education_courses_lesson.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _homework=homework,
                           _data=data, _homework_chat=homework_chat, _user=user, _course=course,
                           _error_message=error_message,
                           _neighboring_lessons=neighboring_lessons, _status_code=status_code, _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/education_home_tasks', methods=['GET', 'POST'])
@login_required
def education_home_tasks():
    """
    Проверка домашних работ и переход в чат с пользователями

    Returns:
        
    """

    current_user_id = flask_login.current_user.user_id
    page_controller = EducationHomeTasksPageController()
    mpc = MainMenuPageController(current_user_id)
    endpoint = request.endpoint

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.main_page"))

    education_streams_list = page_controller.get_education_streams_list()
    user_id = request.args.get('user_id')
    filter_homework = session.get('filter_homework')
    if filter_homework is not None:
        session.pop('filter_homework')
    else:
        filter_homework = 'education_home_tasks'

    id_education_stream = request.args.get('education_stream_id')

    # если ID обучающего потока не найден, то берем ID первого обучающего потока из списка
    if id_education_stream is None:
        id_education_stream = education_streams_list[0]['id']

        education_stream = page_controller.get_current_education_stream(id_education_stream, current_user_id)
        if education_stream['students_list']:
            user_id = education_stream['students_list'][0]['user_id']
        else:
            return redirect(url_for('multilingual.education_home_tasks', education_stream_id=id_education_stream))

        return redirect(url_for('multilingual.education_home_tasks', education_stream_id=id_education_stream,
                                user_id=user_id))
    else:
        id_education_stream = int(id_education_stream)

    if request.method == 'POST':
        if request.form.get('button') == 'id_education_stream':
            id_education_stream = request.form['education_stream']
            education_stream = page_controller.get_current_education_stream(id_education_stream, current_user_id)
            if education_stream['students_list']:
                user_id = education_stream['students_list'][0]['user_id']
            else:
                return redirect(url_for('multilingual.education_home_tasks', education_stream_id=id_education_stream))

        elif request.form.get('button') == 'filter_homework':
            session['filter_homework'] = request.form['filter_homework']

        elif request.form.get('user_id'):
            user_id = request.form.get('user_id')

        return redirect(
            url_for('multilingual.education_home_tasks', education_stream_id=id_education_stream, user_id=user_id))

    # если есть ID пользователя, то возвращаем список домашних работ по фильтрам
    # (по умолчанию - непроверенные домашние работы)

    current_education_stream = page_controller.get_current_education_stream(id_education_stream, current_user_id)
    if user_id is None:
        if current_education_stream['students_list']:
            user_id = current_education_stream['students_list'][0]['user_id']

            return redirect(
                url_for('multilingual.education_home_tasks', education_stream_id=id_education_stream, user_id=user_id))

        user = None
    else:
        user = page_controller.get_user(user_id)

    # список чатов по урокам, по которым не сданы домашние работы
    if filter_homework == 'chat_without_homework':
        data = page_controller.get_chat_without_homework(current_user_id, id_education_stream, user_id)
    # список проверенных домашних работ
    elif filter_homework == 'homework_verified':

        data = page_controller.get_homework_verified(current_user_id, id_education_stream, user_id)
    # список непроверенных домашних работ
    elif filter_homework == 'education_home_tasks':
        data = page_controller.get_homework_no_verified(current_user_id, id_education_stream, user_id)
    else:
        data = None

    return render_template('education_home_tasks.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _data=data,
                           _education_streams_list=education_streams_list, _id_education_stream=id_education_stream,
                           _current_education_stream=current_education_stream, _user=user,
                           _current_filter_homework=filter_homework,
                           _filters_homework_list=config.FILTERS_HOMEWORK_LIST, _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/education_home_task_card', methods=['GET', 'POST'])
@login_required
def education_home_task_card():
    """
    Общение с пользователями, которые сдали домашнюю работу(только для кураторов)
    """

    user_id = flask_login.current_user.user_id
    page_controller = EducationHomeworkCardPageController()
    mpc = MainMenuPageController(user_id)
    endpoint = "education_home_tasks"

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.main_page"))

    id_homework = request.args.get("id_homework")
    id_homework_chat = request.args.get("id_chat")

    data = None
    homework = None
    if id_homework is not None:
        homework = page_controller.get_homework(int(id_homework))
        if homework is not None:
            data = page_controller.get_data_by_id_homework(int(id_homework))
    elif id_homework_chat is not None:
        data = page_controller.get_data_by_id_homework_chat(id_homework_chat, user_id)

    user = page_controller.get_user_by_id(user_id)
    homework_chat = None
    message_error = session.get('message_error')
    status_code = session.get('status_code')
    if session.get('message_error') is not None:
        session.pop('message_error')

    if session.get('status_code') is not None:
        session.pop('status_code')

    if request.method == "POST":
        if request.form.get("send"):
            text = request.form.get("text")
            if text is not None:
                session['message_error'] = page_controller.add_message({"text": text, "id_user": user_id},
                                                                       data['module']['lesson']['id'],
                                                                       data['user']["id"])
                if session['message_error'] is not None:
                    session['status_code'] = "Error"

        elif request.form.get("button") == "answer":
            answer = request.form.get("answer")
            if answer == "True":
                session['message_error'], session['status_code'] = page_controller.homework_answer_accepted(
                    homework["id"], user_id)
            elif answer == "False":
                session['message_error'], session['status_code'] = page_controller.homework_answer_no_accepted(
                    homework["id"], user_id)

        if homework is None:
            return redirect(url_for('multilingual.education_home_task_card', id_chat=id_homework_chat))
        else:
            return redirect(url_for('multilingual.education_home_task_card', id_homework=id_homework))

    if data is not None:
        if id_homework is not None:
            if homework is not None:
                homework_chat = page_controller.get_homework_chat_by_id_homework(int(id_homework), homework['id_user'])
        else:
            homework_chat = page_controller.homework_chat_entry(int(id_homework_chat), data['user']['id'])

    return render_template('education_home_task_card.html', view="corrections", _menu=mpc.get_main_menu(), _user=user,
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _homework_chat=homework_chat, _lang_code=get_locale(), _languages=config.LANGUAGES,
                           _homework=homework, _data=data, _message_error=message_error, _status_code=status_code)


@multilingual.route('/corrections', methods=['GET', 'POST'])
@login_required
def corrections():
    """
    Просмотр выполнение нейро-психологических коррекций

    Returns:
        
    """

    page_controller = CorrectionsPageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    endpoint = request.endpoint

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.evolution_centre_dummy"))

    return render_template('corrections.html', view="corrections", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data=page_controller.get_data(), _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/protocols', methods=['GET', 'POST'])
@login_required
def protocols():
    """
    Просмотр проведение нейро-психологических проб

    Returns:
        
    """

    page_controller = ProbesPageController()

    user_id = flask_login.current_user.user_id
    mpc = MainMenuPageController(user_id)

    endpoint = "protocols"

    probes_list = page_controller.get_probes_list()
    probationers_list = page_controller.get_probationers_list(user_id)

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.evolution_centre_dummy"))

    if request.method == 'POST':
        if request.form.get('button') == 'add_protocol':
            probationer_id = request.form.get('probationer')
            probe_id = request.form.get('probe')

            protocol_id = page_controller.add_protocol(probationer_id, probe_id, user_id)

            return redirect(url_for('multilingual.protocol_card', protocol_id=protocol_id, probe_id=probe_id))

    return render_template('protocols.html', view="probes", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data=page_controller.get_probes(user_id), _is_probationer=page_controller.is_probationers(user_id),
                           _lang_code=get_locale(), _languages=config.LANGUAGES, _probes_list=probes_list,
                           _probationers_list=probationers_list)


@multilingual.route('/protocol_card', methods=['GET', 'POST'])
@login_required
def protocol_card():
    user_id = flask_login.current_user.user_id
    page_controller = ProbeProfileController()
    mpc = MainMenuPageController(user_id)

    endpoint = "protocols"

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.evolution_centre_dummy"))

    protocol_id = request.args.get('protocol_id')
    if protocol_id is not None:
        protocol_id = int(protocol_id)

    probe_id = request.args.get('probe_id')
    if probe_id is not None:
        probe_id = int(probe_id)

    test_list = []
    probationers = []
    protocol = ""

    data = page_controller.get_protocol(protocol_id)
    if data is not None:
        protocol = data["protocol_status"]
    else:
        protocol = None

    test_list = page_controller.get_tests_list(probe_id)

    if request.method == "POST":
        grades = [{"id": key, "grade": value} for key, value in request.form.items() if
                  key.isdigit() or ("_" in key and key.split("_")[0].isdigit())]
        page_controller.add_grades_in_probe(grades, protocol_id)

        if request.form.get("button") == "draft" or request.form.get("button") == "end":
            protocol_status = request.form["button"]
            page_controller.add_grades_in_probe(grades, protocol_id, protocol_status)

            return redirect(url_for("multilingual.protocols"))

        elif request.form["action"]:
            page_controller.add_grades_in_probe(grades, protocol_id)

            return redirect(
                url_for("multilingual.protocol_card", protocol_id=protocol_id))

    return render_template('probe_card.html', view="probe_profile", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _probationers_list=probationers, _data=data,
                           _probes=test_list, _protocol=protocol, _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    """
    Просмотр результатов тестирования

    Returns:
        
    """

    page_controller = ResultsPageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    endpoint = "results"

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.evolution_centre_dummy"))

    return render_template('results.html', view="results", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data=page_controller.get_data(), _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/probationers', methods=['GET', 'POST'])
@login_required
def probationers():
    """
    Просмотр списка испытуемых

    Returns:
        
    """

    user_id = flask_login.current_user.user_id
    endpoint = "probationers"

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.evolution_centre_dummy"))

    page_controller = ProbationersPageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)
    profile_page_controller = ProbationerCardPageController()

    probationer_id = request.args.get('probationer_id')
    error = None
    error_type = {}

    mode = {0: "new"}
    data_edit = {}
    data = {0: profile_page_controller.get_probationer_card_view('')}
    data[0]['probationer_id'] = 0
    num_page = 0

    user_login = UserProfilePageController().get_users_profile_view(user_id)['login']
    probationers_list = page_controller.get_probationers_list_view(user_id)

    for i_probationer in probationers_list:
        if i_probationer is not None and not request.form.get(f"button_{i_probationer['probationer_id']}"):
            mode[i_probationer['probationer_id']] = "view"
        else:
            mode[i_probationer['probationer_id']] = "edit"

        # if probationer_id is None:
        #     mode[i_probationer['probationer_id']] = "new"
        #     probationer_id = ""

        data[i_probationer['probationer_id']] = profile_page_controller.get_probationer_card_view(
            i_probationer['probationer_id'])
        error_type[i_probationer['probationer_id']] = None

    try:
        if request.method == 'POST':
            for i_probationer in probationers_list:
                if request.form.get(f'button_{i_probationer["probationer_id"]}') is not None:
                    probationer_id = i_probationer["probationer_id"]
                    break

            if request.form.get("button_0") is not None:
                probationer_id = 0

            num_page = user_id // 10

            if request.form[f"button_{probationer_id}"] == "add":
                if mode[probationer_id] == "new":
                    # добавляем нового тестируемого и получаем список с ошибками
                    # если их нет, то получаем пустой список
                    probationer = {}
                    probationer["name_probationer"] = request.form[f"name_probationer_{probationer_id}"]
                    probationer["date_of_birth"] = request.form[f"date_of_birth_{probationer_id}"]
                    probationer["name_parent"] = request.form[f"name_parent_{probationer_id}"]
                    probationer["educational_institution"] = request.form[f"educational_institution_{probationer_id}"]
                    probationer["contacts"] = request.form[f"contacts_{probationer_id}"]
                    probationer["diagnoses"] = request.form[f"diagnoses_{probationer_id}"]
                    probationer["reasons_for_contact"] = request.form[f"reasons_for_contact_{probationer_id}"]

                    error = profile_page_controller.create_probationers(user_login, probationer["name_probationer"],
                                                                        probationer["date_of_birth"],
                                                                        probationer["name_parent"],
                                                                        probationer["educational_institution"],
                                                                        probationer["contacts"],
                                                                        probationer["diagnoses"],
                                                                        probationer["reasons_for_contact"], user_id)

                    if error is None:
                        probationers_list = page_controller.get_probationers_list_view(user_id)
                        mode[len(probationers_list)] = "view"
                        error = "Испытуемый сохранён!"
                        error_type[len(probationers_list)] = "Successful"

                        data_edit = data
                        data_edit[len(probationers_list)] = probationer

            elif request.form[f"button_{probationer_id}"] == "edit":
                if mode[probationer_id] == "view":
                    mode[probationer_id] = "edit"

            elif request.form[f"button_{probationer_id}"] == "save":
                if mode[probationer_id] == "edit":
                    probationer = {}

                    probationer["name_probationer"] = request.form[f"name_probationer_{probationer_id}"]
                    probationer["date_of_birth"] = request.form[f"date_of_birth_{probationer_id}"]
                    probationer["name_parent"] = request.form[f"name_parent_{probationer_id}"]
                    probationer["educational_institution"] = request.form[f"educational_institution_{probationer_id}"]
                    probationer["contacts"] = request.form[f"contacts_{probationer_id}"]
                    probationer["diagnoses"] = request.form[f"diagnoses_{probationer_id}"]
                    probationer["reasons_for_contact"] = request.form[f"reasons_for_contact_{probationer_id}"]

                    profile_page_controller.change_probationer(probationer_id, probationer["name_probationer"],
                                                               probationer["date_of_birth"], probationer["name_parent"],
                                                               probationer["educational_institution"],
                                                               probationer["contacts"], probationer["diagnoses"],
                                                               probationer["reasons_for_contact"], user_id)

                    probationers_list = page_controller.get_probationers_list_view(user_id)
                    data_edit = data
                    data_edit[probationer_id] = probationer
                    mode[probationer_id] = "view"
                    error = "Изменения сохранены!"
                    error_type[probationer_id] = "Successful"

            elif request.form[f'button_{probationer_id}'] == "cancel":
                if probationer_id != 0:
                    mode[probationer_id] = "view"

    except exceptions.BadRequestKeyError:

        mode = "view"

    if data_edit == {}:
        data_edit = data

    probationers_list.append(data[0])

    return render_template('probationers.html', view="probationers", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _probationers_list=probationers_list,
                           _is_current_user_admin=flask_login.current_user.is_admin(), _mode=mode,
                           _data=data, _data_edit=data_edit, _error=error, _error_type=error_type,
                           _settings=profile_page_controller.get_settings_probationer(), _num_page=num_page,
                           _lang_code=get_locale(), _languages=config.LANGUAGES)


@multilingual.route('/probationer_card', methods=['GET', 'POST'])
@login_required
def probationer_card():
    """
        Страница просмотра, редактирования и добавления карточки испытуемого
    """

    endpoint = "probationers"

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.evolution_centre_dummy"))

    page_controller = ProbationerCardPageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    probationer_id = request.args.get('probationer_id')
    error = None
    error_type = None

    if probationer_id is not None and not request.form.get("button"):
        mode = "view"
    else:
        mode = "edit"

    if probationer_id is None:
        mode = "new"
        probationer_id = ""

    user_id = flask_login.current_user.user_id
    user_login = UserProfilePageController().get_users_profile_view(user_id)['login']

    data_begin = page_controller.get_probationer_card_view(probationer_id)
    data = {}

    try:
        if request.method == 'POST':
            if request.form["button"] == "add":
                if mode == "new":
                    # добавляем нового тестируемого и получаем список с ошибками
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
                                                                probationer["date_of_birth"],
                                                                probationer["name_parent"],
                                                                probationer["educational_institution"],
                                                                probationer["contacts"], probationer["diagnoses"],
                                                                probationer["reasons_for_contact"])

                    if error is None:
                        mode = "view"
                        error = gettext("Испытуемый сохранён!")
                        error_type = "Successful"

                    data = probationer
            elif request.form["button"] == "edit":
                if mode == "view":
                    mode = "edit"
            elif request.form["button"] == "save":
                if mode == "edit":
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
                    error = gettext("Изменения сохранены!")
                    error_type = "Successful"

    except exceptions.BadRequestKeyError:
        mode = "view"

    if data == {}:
        data = data_begin

    return render_template('probationer_card.html', view="probationer_card", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _data=data,
                           _mode=mode, _data_begin=data_begin, _error=error, _error_type=error_type,
                           _settings=page_controller.get_settings_probationer(), _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/settings/age_range_list', methods=['GET', 'POST'])
@login_required
def age_range_list():
    """
    Генерация страницы просмотра списка диапазонов возрастов

    Returns:

    """

    page_controller = AgeRangeListPageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.main_page"))

    endpoint = request.endpoint

    return render_template('age_range_list.html', view="age_range_list", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _ranges_age=page_controller.get_age_ranges(),
                           _is_current_user_admin=flask_login.current_user.is_admin(), _endpoint=endpoint,
                           _lang_code=get_locale(), _languages=config.LANGUAGES)


@multilingual.route('/settings/maintenance', methods=['GET', 'POST'])
@login_required
def maintenance():
    """
    Controller for maintenance page

    Returns:

    """

    current_user_id = flask_login.current_user.user_id
    page_controller = MaintenancePageController()
    mpc = MainMenuPageController(current_user_id)
    upload_users_from_json_to_sql_page_data = page_controller.get_upload_users_from_json_to_sql_page_data(
        current_user_id)

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.main_page"))

    endpoint = request.endpoint

    if request.method == "POST":
        action_name = request.form['submit_button']

        if action_name == "upload_users_from_json_to_sql":
            page_controller.upload_users_from_json_to_sql(current_user_id)

    return render_template('maintenance.html', view="maintenance", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _endpoint=endpoint, _page_data=upload_users_from_json_to_sql_page_data, _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/settings/estimated_values', methods=['GET', 'POST'])
@login_required
def estimated_values():
    """
    Генерация страницы редактирования оценочных значений

    Returns:

    """
    user_id = flask_login.current_user.user_id
    page_controller = EstimatedValuesPageController()
    mpc = MainMenuPageController(user_id)

    if not flask_login.current_user.is_admin():
        return redirect("multilingual.main_page")

    endpoint = request.endpoint
    id_file_name = request.args.get("id")

    if id_file_name is not None:
        data = page_controller.get_assessments(int(id_file_name))
    else:
        return redirect(url_for("multilingual.estimated_values", id=1))

    if request.method == "POST":
        id_file_name = int(request.form["action"])

        if request.form.get("save") is not None:
            criteria = []

            for i in range(1, 214):
                criteria.append(request.form["{}_grade".format(i)])

            page_controller.overwrite(id_file_name, criteria, user_id)
            data = page_controller.get_assessments(id_file_name)
        else:
            return redirect(url_for("multilingual.estimated_values", id=id_file_name))

    return render_template('estimated_values.html', view="estimated_values", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _data=data, _ranges_age=page_controller.get_age_ranges(), _id_file_name=int(id_file_name),
                           _is_current_user_admin=flask_login.current_user.is_admin(), _endpoint=endpoint,
                           _lang_code=get_locale(), _languages=config.LANGUAGES)


@multilingual.route('/education_streams', methods=['GET', 'POST'])
@app.route('/education_streams', methods=['GET', 'POST'])
@login_required
def education_streams():
    page_controller = EducationStreamsPageController()
    endpoint = "education_streams"
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    education_streams_list = page_controller.get_education_streams()

    return render_template('education_streams.html', view="education_streams", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint),
                           _education_streams_list=education_streams_list, _endpoint=endpoint, _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/education_stream_card', methods=['GET', 'POST'])
@app.route('/education_stream_card', methods=['GET', 'POST'])
@login_required
def education_stream_card():
    endpoint = "education_streams"

    page_controller = EducationStreamPageController()
    mpc = MainMenuPageController(flask_login.current_user.user_id)

    user_id = flask_login.current_user.user_id

    if not flask_login.current_user.is_admin():
        return redirect(url_for("multilingual.main_page"))

    id_education_stream = request.args.get('id')
    message_error = session.get('message_error')
    status_code = session.get('status_code')
    if message_error is not None:
        session.pop('message_error')

    if status_code is not None:
        session.pop('status_code')

    if id_education_stream is not None:
        if request.form.get('button') is None:
            mode = 'view'
        else:
            mode = 'edit'

        id_education_stream = int(id_education_stream)
    else:
        mode = 'new'

    education_stream = page_controller.get_education_stream(id_education_stream)
    timetables_list = page_controller.get_timetables_list(id_education_stream)

    if mode != 'view':
        curators_list = page_controller.get_curators_list(user_id)
        students_list = page_controller.get_students_list(user_id)
        courses_list = page_controller.get_courses_list(id_education_stream)

    else:
        # Если пользователь просматривает карточку обучающего потока, то ищем только данные пользователей и курса
        # этого обучающего потока
        curators_list = page_controller.get_curators_list(user_id, education_stream['curators_list'])
        students_list = page_controller.get_students_list(user_id, education_stream['students_list'])
        courses_list = [education_stream['course']]

    if request.method == 'POST':
        if request.form.get("button") == 'new':
            education_stream_new = {
                "name": request.form.get("name"),
                "id_course": int(request.form.get("course").split('_')[-1]),
                "curators_list": [i['id'] for i in curators_list if request.form.get(f'user_{i["id"]}') is not None],
                "students_list": [i['id'] for i in students_list if request.form.get(f'user_{i["id"]}') is not None],
                "teacher": int(request.form.get("teacher")),
                "date_start": request.form.get("date_start"),
                "date_end": request.form.get("date_ends")
            }

            timetables_list = []
            for course in courses_list:
                if course['id'] == education_stream_new['id_course']:
                    for module in course['modules']:
                        timetables_list.append({
                            "id_module": module['id'],
                            'date_start': request.form.get(f'date_start_module_{module["id"]}')
                        })

            id_education_stream, session['message_error'], session[
                'status_code'] = page_controller.create_education_stream(education_stream_new, timetables_list, user_id)

            return redirect(url_for("multilingual.education_stream_card", id=id_education_stream))

        elif request.form.get('button') == 'edit':
            mode = "edit"

        elif request.form.get('button') == "save":
            education_stream_new = {
                "id": education_stream['id'],
                "name": request.form.get("name"),
                "id_course": int(request.form.get("course").split('_')[-1]),
                "curators_list": [i['id'] for i in curators_list if request.form.get(f'user_{i["id"]}') is not None],
                "students_list": [i['id'] for i in students_list if request.form.get(f'user_{i["id"]}') is not None],
                "teacher": int(request.form.get("teacher")),
                "date_start": request.form.get("date_start"),
                "date_end": request.form.get("date_ends")
            }

            timetables_list = []
            for course in courses_list:
                if course['id'] == education_stream_new['id_course']:
                    for module in course['modules']:
                        timetables_list.append({
                            "id_module": module['id'],
                            'date_start': request.form.get(f'date_start_module_{module["id"]}')
                        })

            session['message_error'], session['status_code'] = page_controller.save_education_stream(
                education_stream_new, timetables_list, user_id)

            return redirect(url_for("multilingual.education_stream_card", id=id_education_stream))

    return render_template('education_stream_card.html', view="education_streams", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(endpoint), _endpoint=endpoint,
                           _curators_list=curators_list, _students_list=students_list, _courses_list=courses_list,
                           _mode=mode, _education_stream=education_stream, _timetables_list=timetables_list,
                           _message_error=message_error, _status_code=status_code, _lang_code=get_locale(),
                           _languages=config.LANGUAGES)


@multilingual.route('/download', methods=['GET', 'POST'])
@login_required
def download():
    page_controller = DownloadPageController()

    name_file = request.args.get("name_file")
    id_dataset = request.args.get("id_dataset")
    dataset = request.args.get("dataset")

    path_file = page_controller.get_path_file(dataset, name_file, id_dataset)
    if path_file is not None:
        return send_file(path_file, as_attachment=True)
    else:
        return False


@app.route('/change_language', methods=['GET'])
def change_language():
    """

    """
    lang_code = request.args.get('lang_code')
    if lang_code is not None:
        languages = [language['lang_code'] for language in config.LANGUAGES]
        if lang_code in languages:
            session['lang_code'] = lang_code
            return lang_code


@multilingual.errorhandler(404)
@login_required
def not_found(e):
    """
    Форма обработки ошибки 404

    Args:
        e ([Exeprion]): ошибка

    Returns:

    """

    return render_template("404.html"), 404


app.register_blueprint(multilingual)
babel = Babel(app)
babel.localeselector(get_locale)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
