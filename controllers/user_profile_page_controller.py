from services.user_profile_service import UserProfileService


class UserProfilePageController():

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_users_profile_view(self, _user_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """        

        user_profile_service = UserProfileService()
        return user_profile_service.get_users_profile(_user_id)
