from typing import Union

from services.maintenance_service import MaintenanceService


class MaintenancePageController():
    """
    controller for maintenance page
    """

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def upload_users_from_json_to_sql(self, _current_user_id):
        """
        Uploads users from json file to sql
        @params:
        """
        service = MaintenanceService()
        error = service.upload_users_from_json_to_sql(_current_user_id)
        # if not isinstance(status, tuple):
        if error is None:
            return 'Данные таблицы "users" из TinyDB были перенесены в Postgresql', 'Successful'

    def get_upload_users_from_json_to_sql_page_data(self):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        _data = []

        service = MaintenanceService()
        _data = service.get_upload_models_from_json_to_sql_page_data('users')

        return _data

    def get_upload_models_from_json_to_sql_page_data(self, _models_for_import_to_sql: list):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        _data = {}

        service = MaintenanceService()
        for model in _models_for_import_to_sql:
            _data[model] = service.get_upload_models_from_json_to_sql_page_data(model)

        return _data

    def upload_actions_from_json_to_sql(self):
        """
        Uploads users from json file to sql
        @params:
        """
        service = MaintenanceService()
        error = service.upload_actions_from_json_to_sql()
        if error is None:
            return 'Данные таблицы "action" из TinyDB были перенесены в Postgresql', 'Successful'

    def get_upload_actions_from_json_to_sql_page_data(self, _current_user_id):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        _data = []

        service = MaintenanceService()
        _data = service.get_upload_actions_from_json_to_sql_page_data(_current_user_id)

        return _data

    def create_table_in_sql(self, _table_name: str):
        """
        Create table
        """
        service = MaintenanceService()

        error = service.create_table_in_sql(_table_name)
        if error is None:
            return f'Таблица "{_table_name}" создана в Postgresql', 'Successful'

    def upload_courses_from_json_to_sql(self):
        """
        Get data for page view

        Args:
        """
        _data = []

        service = MaintenanceService()
        # try:
        service.upload_courses_list_from_json_to_sql()
        # except:
        #     return 'Не удалось импортировать данные таблицы "courses_list" из TinyDB в Postgresql', 'Error'

        return 'Данные таблицы "courses_list" из TinyDB импортированы в Postgresql', 'Successful'

    def upload_modules_from_json_to_sql(self):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        _data = []

        service = MaintenanceService()
        # try:
        service.upload_modules_list_from_json_to_sql()
        #
        # except:
        #     return 'Не удалось импортировать данные таблицы "modules" из TinyDB в Postgresql', 'Error'

        return 'Данные таблицы "modules" из TinyDB были перенесены в Postgresql', 'Successful'

    def upload_lessons_from_json_to_sql(self):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        _data = []

        service = MaintenanceService()
        # try:
        service.upload_lessons_list_from_json_to_sql()
        #
        # except:
        #     return 'Не удалось импортировать данные таблицы "lessons" из TinyDB в Postgresql', 'Error'

        return 'Данные таблицы "lessons" из TinyDB были перенесены в Postgresql', 'Successful'

    def upload_homeworks_from_json_to_sql(self):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        _data = []

        service = MaintenanceService()
        # try:
        service.upload_homeworks_list_from_json_to_sql()
        #
        # except:
        #     return 'Не удалось импортировать данные таблицы "homeworks" из TinyDB в Postgresql', 'Error'

        return 'Данные таблицы "homeworks" из TinyDB были перенесены в Postgresql', 'Successful'

    def upload_homework_chat_list_from_json_to_sql(self):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        _data = []

        service = MaintenanceService()
        # try:
        service.upload_homework_chat_list_from_json_to_sql()
        #
        # except:
        #     return 'Не удалось импортировать данные таблицы "homeworks" из TinyDB в Postgresql', 'Error'

        return 'Данные таблицы "homework_chat" из TinyDB были перенесены в Postgresql', 'Successful'

    def upload_message_from_json_to_sql(self):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        _data = []

        service = MaintenanceService()
        # try:
        service.upload_message_from_json_to_sql()
        #
        # except:
        #     return 'Не удалось импортировать данные таблицы "homeworks" из TinyDB в Postgresql', 'Error'

        return 'Данные таблицы "message" из TinyDB были перенесены в Postgresql', 'Successful'
