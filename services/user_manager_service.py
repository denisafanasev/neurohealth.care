from models.user_manager import UserManager

class UserManagerService():
    """
    UserManagerService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_users(self):
        """
        Возвращает список пользователей

        Returns:
            List: список пользователей с типом User
        """        

        users = []

        user_manager = UserManager()
        users = user_manager.get_users()

        return users
    
    def is_current_user_admin(self):
        """
        Возвращает признак того что у текущего пользователя есть права администратора

        Returns:
            Boolean: True если есть права администратора и False если нет
        """        

        user_manager = UserManager()

        result = user_manager.is_current_user_admin()

        return result
    
    def create_user(self, _login, _name, _password, _password2, _email):
        """
        Создает в системе суперпользователя

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _email (String): email пользователя

        """

        user_manager = UserManager()

        user_manager.create_user(_login, _name, _password, _password2, _email, "user")
