from models.user_manager import UserManager


class UserProfileService():

    def init(self):
        pass

    def get_users_profile(self, user_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """
        user_manager = UserManager()
        user = user_manager.get_user_by_id(user_id)
        return user
