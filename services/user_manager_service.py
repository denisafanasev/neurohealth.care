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

    def get_users(self, _user_id, _page):
        """
        Возвращает список пользователей

        Returns:
            List: список пользователей с типом User
        """        

        user_manager = UserManager()
        users = user_manager.get_users(_user_id, _page)

        return users

    def get_numbers_pages(self, _current_user_id):
        """
        Возвращает количество страниц с данными пользователей и количество пользователей
        Args:
            _current_user_id(Int): ID

        Returns:
            data(Dict): количество возможных страниц и количество пользователей
        """
        user_manager = UserManager()

        users_numbers = user_manager.get_numbers_users(_current_user_id)
        if users_numbers is not None:
            numbers_pages = users_numbers / 20
            if users_numbers % 20 != 0:
                numbers_pages = int(numbers_pages + 1)

            data = {
                'users_numbers': users_numbers,
                'numbers_pages': numbers_pages
            }
            return data