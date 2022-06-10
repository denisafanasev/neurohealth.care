import config
from models.user_manager import UserManager

class MainMenuService():
    """
    MainMenuService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def init(self):
        """
        Constructor
        @params:
        """

        pass

    def get_data(self):
        """
        Return main menu structure
        @params:
        """

        user_manager = UserManager()

        menu = config.MAIN_MENU

        menu = menu + config.EDUCATION_MENU + config.EVOLUTION_MENU

        curent_user_role = user_manager.get_user_role(user_manager.get_current_user_id())

        if curent_user_role == "superuser":
            menu = menu  + config.SUPERUSER_MENU

        return menu

    def get_active_menu_item_number(self, _endpoint):
        """
        Return a number of _endpoind element in the menu
        @params:
            _endpoind     - Required  : menu element endpoint (Str)
        """

        i = 0
        menu = self.get_data()

        for item in menu:
            if item['endpoint'] == _endpoint:
                try:
                    i = item['value']
                    break
                except Exception as e:
                    pass

        return i
