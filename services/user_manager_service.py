from models.user_manager import UserManager
from models.education_stream_manager import EducationStreamManager
from models.action_manager import ActionManager

class UserManagerService():
    """
    UserManagerService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_users(self, _user_id):
        """
        Возвращает список пользователей

        Returns:
            List: список пользователей с типом User
        """        

        user_manager = UserManager()
        users = user_manager.get_users(_user_id)

        return users