import utils.ada as ada
from services.user_manager_service import UserManagerService
from error import UserManagerException


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

    def get_users_list_view(self):
        """
        Возвращает отформатированный список пользователей

        Returns:
            List: список пользователей, каждый из которых представлен структурой типа Dict
        """ 

        user_manager_service = UserManagerService()
        users = user_manager_service.get_users()

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

            users_list_view.append(user_view)
            
        return users_list_view
