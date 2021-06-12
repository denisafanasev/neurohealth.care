import utils.ada as ada
from services.main_page_service import MainPageService


class MainPageController():
    """
    MainPageController - класс контроллера представления главной страницы приложения, реализующий логику взаимодейтвия приложения с пользователем
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
        index_service = MainPageService()
        return index_service.get_data()
