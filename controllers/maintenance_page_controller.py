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
    
    def get_upload_users_from_json_to_sql_page_data(self, _current_user_id):
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """     
        _data = []

        service = MaintenanceService()
        _data = service.get_upload_users_from_json_to_sql_page_data(_current_user_id)

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

    def create_table_in_sql(self, _table_name):
        """

        """
        service = MaintenanceService()

        error = service.create_table_in_sql(_table_name)
        if error is None:
            return f'Таблица "{_table_name}" создана в Postgresql', 'Successful'
