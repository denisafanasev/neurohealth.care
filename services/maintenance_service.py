from distutils.command.config import config

from sqlalchemy import text

from models.action_manager import ActionManager
from models.user_manager import UserManager
from data_adapters.data_store import DataStore

import config

class MaintenanceService():
    """
    Service for maintenance page
    """
    
    def init(self):
        """
        Constructor
        """        
        pass

    def get_upload_users_from_json_to_sql_page_data(self, _current_user_id):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        _data = []

        data_store_tinydb = DataStore('users')
        users_number = data_store_tinydb.get_rows_count()

        data_store_postgresql = DataStore("users", force_adapter="PostgreSQLDataAdapter")
        current_data_adapter = data_store_postgresql.get_current_data_adapter()
        if current_data_adapter == 'PostgreSQLDataAdapter':
            db_users_number = data_store_postgresql.get_rows_count()
            is_there_table = 'Created'
        else:
            db_users_number = None
            is_there_table = 'No created'

        _data = {}
        _data["data_folder"] = config.DATA_FOLDER
        _data["users_number"] = users_number
        _data["PostgreSQLDataAdapter_connection_string"] = config.PostgreSQLDataAdapter_connection_string()
        _data["current_data_adapter"] = current_data_adapter
        _data["db_users_number"] = db_users_number
        _data["is_there_table"] = is_there_table

        return _data

    def upload_users_from_json_to_sql(self, _current_user_id):
        """
        Uploads users from json file to sql
        @params:
        """
        
        # get all users in the system
        user_manager = UserManager()
        data_store_tiny_db = DataStore('users')
        if user_manager.get_user_role(_current_user_id) == 'superuser':
            users = data_store_tiny_db.get_rows()
        else:
            users = []

        # create data store with SQL data adapter
        data_store = DataStore("users", force_adapter="PostgreSQLDataAdapter")
        for user_data in users:
            user = user_manager.user_row_to_user(user_data)
            if user.token == '':
                user.token = user_manager.create_token(user.email)
            # convert User object to Dict
            user_raw = {"doc_id": user.user_id, "active": user.active, "password": user_data['password'], "created_date": user.created_date,
                            "education_module_expiration_date": user.education_module_expiration_date, "email": user.email,
                            "email_confirmed": user.email_confirmed, "login": user.login, "name": user.name,
                            "probationers_number": user.probationers_number, "role": user.role, "token": user.token}

            if data_store.get_row_by_id(user.user_id):

                # if user existed in the table, make change
                data_store.update_row_by_id(user_raw, user.user_id)

            else:

                # if user non existed, make insert of a new row
                data_store.insert_row(user_raw)

    def get_upload_actions_from_json_to_sql_page_data(self, _current_user_id):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        _data = []

        data_store_tinydb = DataStore("action")
        actions_number = data_store_tinydb.get_rows_count()

        data_store_postgresql = DataStore("action", force_adapter="PostgreSQLDataAdapter")
        current_data_adapter = data_store_postgresql.get_current_data_adapter()
        if current_data_adapter == 'PostgreSQLDataAdapter':
            db_actions_number = data_store_postgresql.get_rows_count()
            is_there_table = 'Created'
        else:
            db_actions_number = None
            is_there_table = 'No created'

        _data = {}
        _data["data_folder"] = config.DATA_FOLDER
        _data["actions_number"] = actions_number
        _data["PostgreSQLDataAdapter_connection_string"] = config.PostgreSQLDataAdapter_connection_string()
        _data['current_data_adapter'] = data_store_postgresql.get_current_data_adapter()
        _data["db_actions_number"] = db_actions_number
        _data['is_there_table'] = is_there_table

        return _data

    def upload_actions_from_json_to_sql(self):
        """
        Uploads actions  from json file to sql
        @params:
        """

        # get all actions in the system
        action_manager = ActionManager()
        data_store_tinydb = DataStore('action')
        user_manager = UserManager()

        action_list = data_store_tinydb.get_rows()

        # create data store with SQL data adapter
        data_store_postgresql = DataStore("action", force_adapter="PostgreSQLDataAdapter")

        for action_data in action_list:
            # convert Action object to Dict
            action = action_manager.action_row_to_action(action_data)
            user = user_manager.get_user_by_login(action.user_login)
            if user is not None:
                action_raw = {"doc_id": action.id, 'user_id': user.user_id, 'action': action.action,
                              'created_date': action.created_date, 'comment_action': action.comment_action}
                if data_store_postgresql.get_row_by_id(action.id):
                    # if action existed in the table, make change
                    data_store_postgresql.update_row_by_id(action_raw, action.id)
                else:
                    # if action non existed, make insert of a new row
                    data_store_postgresql.insert_row(action_raw)

    def create_table_in_sql(self, _table_name):
        """
        Создает таблицу в PostgreSQL

        Args:
            _table_name(Str): имя таблицы

        Returns:
            None
        """
        # Подключаемся к БД
        data_store = DataStore(None, force_adapter="PostgreSQLDataAdapter")
        # Читаем файл, в котором есть sql скрипты для создания таблиц
        with open('database/neurohealth.sql', 'r') as sql_file:
            sql_text = sql_file.read()

        sql_scripts_list = sql_text.split('\n\n')
        # Ищем нужный и после создаем таблицу
        for sql_script in sql_scripts_list:
            if _table_name in sql_script:
                data_store.data_store.data_store.execute(text(sql_script))
                break
