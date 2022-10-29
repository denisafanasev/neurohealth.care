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

    def upload_users_from_json_to_sql(self, _user_id):
        """
        Uploads users from json file to sql
        @params:
        """
        service = MaintenanceService()
        service.upload_users_from_json_to_sql(_user_id)
