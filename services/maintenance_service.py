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

            user_raw = {"user_id": user.user_id, "active": user.active, "create_data": user.created_date,
                        "education_module_expiration_date": user.education_module_expiration_date, "email": user.email,
                        "email_confirmed": user.email_confirmed, "login": user.login, "name": user.name,
                        "probationers_number": user.probationers_number, "role": user.role, "token": user.token}

            data_store.add_row(user_raw)
