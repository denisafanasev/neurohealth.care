import sentry_sdk

from flask import Flask, request, redirect, url_for, render_template, make_response, send_file, session
from flask import g
from flask_login import LoginManager, login_required, login_user, logout_user

from sentry_sdk.integrations.flask import FlaskIntegration

import os
import time
import datetime
import logging
from logging.handlers import RotatingFileHandler

# general page controllers
from controllers.index_page_controller import IndexPageController
from controllers.main_menu_controller import MainManuPageController
from controllers.login_page_controller import LoginPageController

from error import UserManagerException

import utils.ada as ada
import config

sentry_sdk.init(
    dsn="https://63b5f6ab88514c9cb9ab336e34d42590@o640301.ingest.sentry.io/5756937",
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


@app.context_processor
def inject_global_context():
    return dict(app_version=config.VERSION)


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
    division_by_zero = 1 / 0

@app.route("/logout")
@login_required
def logout():
    """
    Страница выхода пользователя из системы

    Returns:
        
    """    

    logout_user()
    return redirect('index')

@app.route('/create_superuser', methods=['GET', 'POST'])
def create_superuser():
    """
    форма создания суперпользоватля при первой запуске системы без сформировного списка пользователей

    Returns:
        
    """    

    login_page_controller = LoginPageController()

    # если в системе есть созданный список пользователей, то выполняем процедуру авторизации, если нет, то создаем первого суперпользователя
    if login_page_controller.is_there_users():

        # пользователей есть, отправляемся на авторизацию
        return redirect('login')
    
    # пользователей нет, будем создавать нового администратора
    error_message = ""

    if request.method == 'POST':

        login = request.form['superuser_login']
        name = request.form['superuser_name']
        password = request.form['superuser_password']
        password_2 = request.form['superuser_password_2']
        email = request.form['superuser_email']

        try:

            login_page_controller.create_superuser(login, name, password, password_2, email)
            return render_template('create_superuser.html', view="create_superuser", _superuser_created=True, _error_message=error_message)

        except UserManagerException as e:

            error_message = str(e)

    return render_template('create_superuser.html', view="create_superuser", _superuser_created=False, _error_message=error_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Форма входа пользователя в систему (ввод логина и пароля)

    Returns:
        
    """    

    login_page_controller = LoginPageController()

    # если в системе есть созданный список пользователей, то выполняем процедуру авторизации, если нет, то создаем первого суперпользователя
    if not login_page_controller.is_there_users():

        # пользователей нет, надо создать первого суперпользователя
        return redirect('create_superuser')
        pass

    # пользователи есть, проходим процедуру идентификации
    login_error = False

    if request.method == 'POST':

        login = request.form['login']
        password = request.form['password']

        user = login_page_controller.get_user(login, password)

        if user is not None:
            login_user(user)
            return redirect('index')
        else:
            login_error = True

    return render_template('login.html', view="login", _login_error=login_error)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    ipc = IndexPageController()
    mpc = MainManuPageController()

    endpoint = request.endpoint

    return render_template('index.html', view="dashboard", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data=ipc.get_data())


@app.route('/user_manager', methods=['GET', 'POST'])
@login_required
def user_manager():
    """
    Страница управления списков пользователей системы

    Returns:
        
    """    

    ipc = IndexPageController()
    mpc = MainManuPageController()

    endpoint = request.endpoint

    return render_template('index.html', view="dashboard", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data=ipc.get_data())
                               

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
