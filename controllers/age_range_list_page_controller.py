from services.age_range_list_service import AgeRangeListsService

class AgeRangeListPageController():
    """
    AgeRangeListPageController - класс контроллера представления просмотра списка диапазонов возрастов,
     реализующий логику взаимодейтвия приложения с пользователем
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответсвующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    def __init__(self):
        """
        Constructor
        @params:
        """
        pass

    def get_age_ranges(self):
        """
        Возвращает список диапазонов возрастов

        Returns:
            List: список диапазонов возрастов
        """

        page_service = AgeRangeListsService()

        return page_service.get_age_ranges()
