from flask import Flask, request, redirect, url_for, render_template, make_response, send_file, session
from flask import g
from flask_login import LoginManager, login_required, login_user, logout_user
import os
import time
import datetime
import logging
from logging.handlers import RotatingFileHandler

# general page controllers
from controllers.index_page_controller import IndexPageController
from controllers.main_menu_controller import MainManuPageController

import utils.ada as ada
import config

from services.login_service import LoginService


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

    login_service = LoginService()
    user = login_service.get_user(user_id)

    return user


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('index')


@app.route('/login', methods=['GET', 'POST'])
def login():

    login_error = False

    if request.method == 'POST':

        login = request.form['login']
        password = request.form['password']

        login_service = LoginService()
        user_id = login_service.get_user_id(login, password)
        user = login_service.get_user(user_id)

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

    ipc = IndexPageController()
    mpc = MainManuPageController()

    endpoint = request.endpoint

    return render_template('index.html', view="dashboard", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data=ipc.get_data())
                               

@app.route('/application_log', methods=['GET', 'POST'])
@login_required
def application_log():

    alpc = ApplicationLogPageController()
    mpc = MainManuPageController()

    endpoint = request.endpoint
    session["main_menu_page"] = mpc.get_active_menu_item_number(endpoint)

    if request.method == 'POST':
        action = request.form['action']
        if action == 'clear_application_log':
            alpc.clear_log()

    return render_template('application_log.html', view="application_log", _menu=mpc.get_main_menu(),
                           _active_main_menu_item=mpc.get_active_menu_item_number(
                               endpoint), _data=alpc.get_data())


@app.errorhandler(404)
@login_required
def not_found(e):
    """Page not found."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
