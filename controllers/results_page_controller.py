import utils.ada as ada
from services.results_service import ResultsService


class ResultsPageController():
    """
    ResultsPageController - класс контроллера представления списка результатов проб, реализующий логику взаимодейтвия приложения с пользователем
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
        page_service = ResultsService()
        return page_service.get_data()
