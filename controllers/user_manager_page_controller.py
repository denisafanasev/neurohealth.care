import utils.ada as ada
from services.user_manager_service import UserManagerService


class UserManagerPageController():
    """
    UserManagerPageController - класс контроллера представления управления списком пользователей системы
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответсвующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_users_list_view(self, _user_id, _filters):
        """
        Возвращает отформатированный список пользователей

        Returns:
            List: список пользователей, каждый из которых представлен структурой типа Dict
        """ 

        user_manager_service = UserManagerService()

        users = user_manager_service.get_users(_user_id, _filters)
        users_list_view = []
        for user in users:

            user_view = {}

            user_view['user_id'] = user.user_id
            user_view['login'] = user.login
            user_view['name'] = user.name
            user_view['email'] = user.email
            user_view['role'] = user.role
            user_view['created_date'] = str(user.created_date.strftime("%d/%m/%Y"))
            user_view['education_module_expiration_date'] = str(user.education_module_expiration_date.strftime("%d/%m/%Y"))
            user_view['probationers_number'] = user.probationers_number
            user_view['is_active'] = user.active
            user_view['active_education_module'] = user.active_education_module
            user_view['email_confirmed'] = user.email_confirmed

            users_list_view.append(user_view)
            
        return users_list_view

    def get_number_of_users_with_subscriptions(self, _user_id):
        """
        Возвращает количество пользователей с активной подпиской/ролью user

        Args:
            _user_id(Int): ID текущего пользователя

        Returns:
            number_of_users_with_subscriptions: количество пользователей с подпиской
            number_of_users: количество пользователей с ролью user
        """

        user_manager_service = UserManagerService()

        return user_manager_service.get_number_of_users_with_subscriptions(_user_id)


