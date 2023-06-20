from distutils.command.config import config

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

        user_manager = UserManager()
        users = user_manager.get_users(_current_user_id)
        users_number = len(users)

        db_data_store = DataStore("users", force_adapter="PostgreSQLDataAdapter")
        db_users_number = db_data_store.get_rows_count()

        _data = {}
        _data["data_folder"] = config.DATA_FOLDER
        _data["users_number"] = users_number
        _data["PostgreSQLDataAdapter_connection_string"] = config.PostgreSQLDataAdapter_connection_string()
        _data["db_users_number"] = db_users_number

        return _data

    def upload_users_from_json_to_sql(self, _current_user_id):
        """
        Uploads users from json file to sql
        @params:
        """
        
        # get all users in the system
        user_manager = UserManager()
        users = user_manager.get_users(_current_user_id)

        # create data store with SQL data adapter
        data_store = DataStore("users", force_adapter="PostgreSQLDataAdapter")
        # data_store_tiny_db = DataStore('users')

        for user in users:
            password = ''

            # user_data = data_store_tiny_db.get_row_by_id(user.user_id)
            # if user_data is not None:
            #     password = user_data['password']

            # convert User object to Dict
            user_raw = {"doc_id": user.user_id, "active": user.active, "password": password, "created_date": user.created_date,
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

        action_manager = ActionManager()
        actions = action_manager.get_actions_by_login(_current_user_id)
        actions_manager = len(actions)

        db_data_store = DataStore("actions", force_adapter="PostgreSQLDataAdapter")
        db_users_number = db_data_store.get_rows_count()

        _data = {}
        _data["data_folder"] = config.DATA_FOLDER
        _data["users_number"] = actions_manager
        _data["PostgreSQLDataAdapter_connection_string"] = config.PostgreSQLDataAdapter_connection_string()
        _data["db_users_number"] = db_users_number

        return _data

    def upload_actions_from_json_to_sql(self):
        """
        Uploads actions from json file to sql
        @params:
        """

        # get all users in the system
        action_manager = ActionManager()
        user_manager = UserManager()

        action_list = action_manager.get_actions()

        # create data store with SQL data adapter
        data_store = DataStore("action", force_adapter="PostgreSQLDataAdapter")

        for action in action_list:
            # convert Action object to Dict
            user = user_manager.get_user_by_login(action.user_login)
            action_raw = {"doc_id": action.id, 'user_id': user.user_id, 'action': action.action,
                          'created_date': action.created_date, 'comment_action': action.comment_action}
            if data_store.get_row_by_id(action.id):

                # if user existed in the table, make change
                data_store.update_row_by_id(action_raw, action.id)

            else:

                # if user non existed, make insert of a new row
                data_store.insert_row(action_raw)
