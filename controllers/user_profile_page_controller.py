import utils.ada as ada
from services.user_profile_service import UserProfileService


class UserProfilePageController():

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_data(self):
        index_service = UserProfileService()
        return index_service.get_data()
