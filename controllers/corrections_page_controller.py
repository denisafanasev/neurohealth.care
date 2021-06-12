import utils.ada as ada
from services.corrections_service import CorrectionsService


class CorrectionsPageController():
    """
    CorrectionsPageController - класс контроллера представления списка коррекций, реализующий логику взаимодейтвия приложения с пользователем
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
        page_service = CorrectionsService()
        return page_service.get_data()
