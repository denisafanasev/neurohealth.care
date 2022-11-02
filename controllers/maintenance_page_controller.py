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
        service.upload_users_from_json_to_sql(_current_user_id)
    
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
