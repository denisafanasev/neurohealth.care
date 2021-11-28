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
            user_view['expires_date'] = str(user.expires_date.strftime("%d/%m/%Y"))

            user_view['probationers_number'] = user.probationers_number

            user_view['is_active'] = user.is_active

            users_list_view.append(user_view)
            
        # TODO: похоже тут не тот список возвращается
        return users_list_view

    def create_user(self, _login, _name, _password, _password2, _email):
        """
        Создает в системе пользователя

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _email (String): email пользователя

        """        

        # создаем суперпользователя
        user_manager_service = UserManagerService()
        user_manager_service.create_user(_login, _name, _password, _password2, _email)