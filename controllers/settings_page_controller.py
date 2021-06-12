import utils.ada as ada
from services.settings__service import SettingsService


class SettingsPageController():
    """
    SettingsPageController - класс контроллера представления настроек приложения, реализующий логику взаимодейтвия приложения с пользователем
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответсвующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_data(self):
        page_service = SettingsService()
        return page_service.get_data()
