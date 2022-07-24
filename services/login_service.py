from models.user_manager import UserManager
from models.action_manager import ActionManager
from error import UserManagerException

class LoginService():
    """
    Класс реализующий бизнес-логику приложения, связанную с процедурами авторизации и идентификации
    Возвращает в слой представления объекты в доменной структуре
    Взаимодейтвует с классами слоя моделей передавая им объекты в доменной структуре
    """    
    
    def get_user_by_id(self, _user_id):
        """
        Возвращает пользователя по заданному ID

        Args:
            _user_id (Int): id пользователя

        Returns:
            User: пользователь
        """       

        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)

        return user
    
    def get_user(self, _login, _password):
        """
        Возвращает пользователя по имени и паролю или None в случае, если пользователь не найден

        Args:
            _login (String): логин пользователя
            _password (String): пароль пользователя

        Returns:
            User: найденный пользователь или None
        """  

        user_manager = UserManager()
        action_manager = ActionManager()

        user = user_manager.get_user(_login, _password)

        # делаем проверки, что пользователь может входить в систему
        if (user.email_confirmed is False) and (user.token != "") and (user.role != "superuser"):
            # raise UserManagerException("Email пользователя не подтвержден")
            pass
            
        if not user.active:
            raise UserManagerException("Данный пользователь заблокирован")
        elif user.role != "superuser":
            action_manager.add_notifications("", "зашел", "", "в систему", user.login)

        return user
    
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

        user_manager.create_user(_login, _name, _password, _password2, _email, _role, _access_time = "бессрочно")
