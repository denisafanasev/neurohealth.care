import utils.ada as ada
from services.probes_service import ProbesService


class ProbesPageController():
    """
    ProbesPageController - класс контроллера представления списка проб, реализующий логику взаимодейтвия приложения с пользователем
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
        page_service = ProbesService()
        return page_service.get_data()
