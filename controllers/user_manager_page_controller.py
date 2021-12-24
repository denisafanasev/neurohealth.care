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
            if not user.expires_date == "неограниченно":
                user_view['expires_date'] = str(user.expires_date.strftime("%d/%m/%Y"))
            else:
                user_view['expires_date'] = user.expires_date

            user_view['probationers_number'] = user.probationers_number

            user_view['is_active'] = user.is_active

            users_list_view.append(user_view)
            
        return users_list_view

    def create_user(self, _login, _name, _password, _password2, _email, _role, _probationers_number, _access_time):
        """
        Создает в системе пользователя

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _email (String): email пользователя
            _role (String): роль пользователя [user/superuser]
            _probationers_number (int): количество доступных тестируемых
            _access_time (String): срок доступа

        Returns:
            String: ошибка при создании пользователя

        """        


        user_manager_service = UserManagerService()
        return user_manager_service.create_user(_login, _name, _password, _password2, _email, _role, _probationers_number, _access_time)

    def change_user(self, _login, _name, _email, _role, _probationers_number, _access_time, _created_date):
        """
        Обновляет информацию о пользователе и возвращает ее

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _email (String): email пользователя
            _role (String): роль пользователя [user/superuser]
            _access_time (String): срок доступа

        Returns:
            Dict: словарь с информацией о пользователе
        """

        user_manager_service = UserManagerService()

        return user_manager_service.change_user(_login, _name, _email, _role, _probationers_number, _access_time, _created_date)

    def discharge_password(self, _login, _password, _password2):
        """
        Обновляет в системе пароль пользователя

        Args:
            _login (String): логин пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя

        Returns:
            String: ошибка при обновлении пароля пользователя

        """

        user_manager_service = UserManagerService()
        try:
            user_manager_service.discharge_password(_login, _password, _password2)
        except UserManagerException as error:
            return error