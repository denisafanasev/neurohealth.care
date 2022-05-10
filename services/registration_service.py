from models.user_manager import UserManager


class RegistrationService():
    """
    Класс реализующий бизнес-логику приложения, связанную с регистрацией нового пользователя
    Возвращает в слой представления объекты в доменной структуре
    Взаимодейтвует с классами слоя моделей передавая им объекты в доменной структуре
    """    
    
    def is_there_users(self):
        """
        Проверяет, есть ли в системе созданные пользователи
        Используется для того что бы определить при входе в систему не нужно ли создавать суперпользователя

        Returns:
            Boolean: True/False в зависимости от того есть в системе пользователи или нет
        """

        user_manager = UserManager()

        if user_manager.is_there_users():
            return True
        
        return False
    
    def create_user(self, _login, _name, _password, _password2, _email, _create_superuser):
        """
        Создает в системе суперпользователя

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _email (String): email пользователя
            _create_superuser (Boolean): признак создания суперпользователя

        """

        user_manager = UserManager()

        _role = "user"
        if _create_superuser:
            _role = "superuser"

        user_manager.create_user(_login, _name, _password, _password2, _email, _role, _probationers_number=5, _access_time = "бессрочно")
