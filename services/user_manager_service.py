from datetime import datetime

from models.user_manager import UserManager


class UserManagerService():
    """
    UserManagerService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_users(self, _user_id, _filters):
        """
        Возвращает список пользователей

        Returns:
            List: список пользователей с типом User
        """        

        user_manager = UserManager()
        if _filters == 'with_subscription':
            users = user_manager.get_users(_user_id, {'role': 'user'})
            user_list = [user for user in users if user.education_module_expiration_date >=datetime.now()]

        else:
            user_list = user_manager.get_users(_user_id)

        return user_list

    def get_number_of_users_with_subscriptions(self, _user_id):
        """
        Возвращает количество пользователей с активной подпиской/ролью user

        Args:
            _user_id(Int): ID текущего пользователя

        Returns:
            number_of_users_with_subscriptions: количество пользователей с подпиской
            number_of_users: количество пользователей с ролью user
        """

        user_manager = UserManager()

        users = user_manager.get_users(_user_id, {'role': 'user'})
        number_of_users_with_subscriptions = 0
        for user in users:
            if user.education_module_expiration_date >= datetime.now():
                number_of_users_with_subscriptions += 1

        return number_of_users_with_subscriptions, len(users)
