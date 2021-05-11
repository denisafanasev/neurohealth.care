import utils.ada as ada
from services.login_service import LoginService


class LoginPageController():
    """
    Класс объекта представления страницы входа в приложение
    Получает от объектов слоя бизнес-логики объекты в доменной структуре и преобразовывает их в типы, пригодные для представления на web странице
    Отвечает за контроль ввода пользователя и реализацию логики взаимодейтвия пользователя с приложением
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
        user = login_service.get_user(_login, _password)

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
        Используется для того что бы определить при входе в систему не нужно ли создавать суперпользователя

        Returns:
            Boolean: True/False в зависимости от того есть в системе пользователи или нет
        """     

        login_service = LoginService()
        return login_service.is_there_users()
    
    def create_superuser(self, _login, _name, _password, _password2, _email):
        """
        Создает в системе суперпользователя

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _email (String): email пользователя

        """        

        # создаем суперпользователя
        login_service = LoginService()
        login_service.create_superuser(_login, _name, _password, _password2, _email)
