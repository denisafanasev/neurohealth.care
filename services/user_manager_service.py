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

    def get_numbers_pages(self, _current_user_id, _search_text):
        """
        Возвращает количество страниц с данными пользователей и количество пользователей
        Args:
            _current_user_id(Int): ID

        Returns:
            data(Dict): количество возможных страниц и количество пользователей
        """
        user_manager = UserManager()

        if not _search_text:
            users_numbers = user_manager.get_numbers_users(_current_user_id)
        else:
            users_numbers = len(user_manager.get_users_by_search_text(_search_text, _current_user_id))

        if users_numbers is not None:
            numbers_pages = int(users_numbers / 20)
            if users_numbers % 20 != 0:
                numbers_pages = numbers_pages + 1

            data = {
                'users_numbers': users_numbers,
                'numbers_pages': numbers_pages
            }
            return data

    def get_users_by_search_text(self, _search_text, _current_user_id, _page):
        """
        Возвращает список пользователей, у которых логин, email или имя пользователя совпадает с текстом

        Args:
            _search_text(Str): текст
            _current_user_id(Int): ID текущего пользователя

        Returns:
            users_list: список пользователей
        """
        user_manager = UserManager()

        return user_manager.get_users_by_search_text(_search_text, _current_user_id, _page)