from models.estimated_values_manager import EstimatedValuesManager

class AgeRangeListsService():
    """
    AgeRangeListsService - класс бизнес-логики сервиса управления просмотром списка диапазонов возрастов
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def init(self):
        pass

    def get_age_ranges(self):
        """
        Возвращает список диапазонов возрастов

        Returns:
            List: список диапазонов возрастов
        """

        estimated_values_manager = EstimatedValuesManager()

        return estimated_values_manager.get_age_ranges()