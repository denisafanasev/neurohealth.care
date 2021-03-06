from models.action_manager import ActionManager
from models.user_manager import UserManager
class MainPageService():
    """
    MainPageService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """
    
    def init(self):
        pass

    def get_data(self):
        return "Data"

    def get_user_by_id(self, _user_id):
        """
        Фукция возвращает пользователя по его id

        Args:
            _user_id (_type_): id пользователя

        Returns:
            User: пользователь
        """        

        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)

        return user

    def discharge_password(self, _login, _password, _password2, _current_user_id, _current_password=''):
        """
        Обновляет в системе пароль пользователя

        Args:
            _login (String): логин пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя

        Returns:
            String: ошибка при обновлении пароля пользователя
        """

        user_manager = UserManager()
        action_manager = ActionManager()

        error = user_manager.discharge_password(_login, _password, _password2, _current_password)
        login_superuser = user_manager.get_user_by_id(_current_user_id).login

        action_manager.add_notifications(_login, "изменил", 'пароль', "user_manager", login_superuser)

        return error

    def get_actions(self, _user_id):

        action_manager = ActionManager()

        return action_manager.get_actions(_user_id)