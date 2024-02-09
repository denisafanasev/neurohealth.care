import pandas as pd

import utils.ada as ada
from services.user_manager_service import UserManagerService
from error import UserManagerException
import config


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

    def get_users_list_view(self, _user_id):
        """
        Возвращает отформатированный список пользователей

        Returns:
            List: список пользователей, каждый из которых представлен структурой типа Dict
        """

        user_manager_service = UserManagerService()

        users = user_manager_service.get_users(_user_id)
        if not isinstance(users, pd.DataFrame):
            users_list_view = []
            for user in users:
                user_view = {}

                user_view['user_id'] = user.user_id
                user_view['login'] = user.login
                user_view['name'] = user.name
                user_view['email'] = user.email
                user_view['role'] = user.role
                user_view['created_date'] = str(user.created_date.strftime("%d/%m/%Y"))
                user_view['education_module_expiration_date'] = str(
                    user.education_module_expiration_date.strftime("%d/%m/%Y"))
                user_view['probationers_number'] = user.probationers_number
                user_view['is_active'] = user.active
                user_view['active_education_module'] = user.active_education_module
                user_view['email_confirmed'] = user.email_confirmed

                users_list_view.append(user_view)
        else:
            
            users.rename(columns={'doc_id': 'user_id', 'active': 'is_active'}, inplace=True)
            users['created_date'] = users['created_date'].dt.strftime('%d/%m/%Y')
            users['education_module_expiration_date'] = users['education_module_expiration_date'].dt.strftime('%d/%m/%Y')
            
            users_list_view = users.to_dict('records')

        return users_list_view

    def get_numbers_pages(self, _current_user_id, _search_text):
        """
        Возвращает количество страниц с данными пользователей и количество пользователей

        Args:
            _current_user_id(Int): ID

        Returns:
            data(Dict): количество возможных страниц и количество пользователей
        """
        user_manager_service = UserManagerService()

        return user_manager_service.get_numbers_pages(_current_user_id, _search_text)

    def get_users_by_search_text(self, _search_text, _current_user_id, _page):
        """
        Возвращает список пользователей, у которых логин, email или имя пользователя совпадает с текстом

        Args:
            _search_text(Str): текст
            _current_user_id(Int): ID текущего пользователя

        Returns:
            users_list: список пользователей
        """
        user_manager_service = UserManagerService()

        users_list = user_manager_service.get_users_by_search_text(_search_text, _current_user_id, _page)

        users_list_view = []
        if users_list is not None:
            for user in users_list:
                user_view = {
                    'user_id': user.user_id,
                    'login': user.login,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role,
                    'created_date': str(user.created_date.strftime("%d/%m/%Y")),
                    'education_module_expiration_date': str(
                        user.education_module_expiration_date.strftime("%d/%m/%Y")),
                    'probationers_number': user.probationers_number,
                    'is_active': user.active,
                    'active_education_module': user.active_education_module,
                    'email_confirmed': user.email_confirmed,
                }

                users_list_view.append(user_view)

        return users_list_view