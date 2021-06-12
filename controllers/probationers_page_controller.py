import utils.ada as ada
from services.probationers_service import ProbationersService


class ProbationersPageController():
    """
    ProbationersPageController - класс контроллера представления списка тестируемых, реализующий логику взаимодейтвия приложения с пользователем
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
        page_service = ProbationersService()
        return page_service.get_data()
