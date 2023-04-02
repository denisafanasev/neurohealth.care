import json

from flask import request

import config
import utils.ada as ada
from services.main_menu_service import MainMenuService


class MainMenuPageController():
    """
    MainMenuPageController - класс контроллера представления главного меню приложения, реализующий логику взаимодейтвия приложения с пользователем
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответсвующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    user_id = None

    def __init__(self, _user_id):
        """
        Constructor
        @params:
        """

        self.user_id = _user_id

    def get_main_menu(self):
        """
        Return main menu structure for visualization
        @params:
        """

        main_menu_service = MainMenuService()
        data = main_menu_service.get_data(self.user_id)
        menu = []

        main_menu = set()
        # получаем список всех модулей для главного меню
        for i, item in enumerate(data):
            main_menu.add(item['module'])

        # main_menu = sorted(main_menu)

        for main_item in main_menu:
            module_menu = []
            for i, item in enumerate(data):
                if item['module'] == main_item:
                    item['value'] = i
                    module_menu.append(item)

            menu.append([main_item, module_menu])

        menu.sort()
        
        return menu

    def get_active_menu_item_number(self, _endpoind):
        """
        Return a number of _endpoind element in the menu
        @params:
            _endpoind     - Required  : menu element endpoint (Str)
        """

        main_menu_service = MainMenuService()
        endpoint = _endpoind.split('.')[-1]
        active_menu_item = main_menu_service.get_active_menu_item_number(self.user_id, endpoint)
        return active_menu_item

    # def get_languages_list(self):
    #     """
    #     Возвращает список доступных языков.
    #     """
    #     if not 'app' in request.host_url:
    #         languages = config.LANGUAGES
    #     else:
    #         languages = [config.LANGUAGES[0]]
    #
    #     return languages

