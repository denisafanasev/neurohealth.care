from models.user_manager import UserManager
from data_adapters.data_store import DataStore

class MaintenanceService():
    """
    Service for maintenance page
    """
    
    def init(self):
        """
        Constructor
        """        
        pass

    def upload_users_from_json_to_sql(self, _user_id):
        """
        Uploads users from json file to sql
        @params:
        """
        
        # get all users in the system
        user_manager = UserManager()
        users = user_manager.get_users(_user_id)

        # create data sttore with SQL data adapter
        data_store = DataStore("users", "PostgreSQLDataAdapter")

        for user in users:
            data_store.add_row({"id": user.id})
