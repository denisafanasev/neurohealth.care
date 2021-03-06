import utils.ada as ada
from services.login_service import LoginService
from error import UserManagerException

class LoginPageController():
    """
    LoginPageController - класс контроллера представления страницы входа в приложение, реализующий логику
    взаимодейтвия приложения с пользователем
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в
    соответсвующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_user(self, _login, _password):
        """
        Возвращает пользователя по имени и паролю или None в случае, если пользователь не найден

        Args:
            _login (String): логин пользователя
            _password (String): пароль пользователя

        Returns:
            User: найденный пользователь или None
        """        

        login_service = LoginService()
        try:
            user = login_service.get_user(_login, _password)
        except UserManagerException as error:
            return error

        return user 

    def get_user_by_id(self, _user_id):
        """
        Возвращает пользователя по заданному ID

        Args:
            _user_id (Int): id пользователя

        Returns:
            User: пользователь
        """

        login_service = LoginService()
        user = login_service.get_user_by_id(_user_id)
        return user

    def is_there_users(self):
        """
        Проверяет, есть ли в системе созданные пользователи
        Используется для того что бы определить при входе в систему не
        нужно ли создавать суперпользователя

        Returns:
            Boolean: True/False в зависимости от того есть в системе пользователи или нет
        """

        login_service = LoginService()
        return login_service.is_there_users()
