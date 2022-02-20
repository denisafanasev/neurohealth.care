from models.estimated_values_manager import EstimatedValuesManager

class EstimatedValuesService():
    """
    SettingsService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_assessments(self, _file_name):

        estimated_values_manager = EstimatedValuesManager()

        return estimated_values_manager.get_assessments(_file_name)

    def get_age_ranges(self):

        estimated_values_manager = EstimatedValuesManager()

        return estimated_values_manager.get_age_ranges()

    def overwrite(self, _file_name, _criteria):

        estimated_values_manager = EstimatedValuesManager()

        return estimated_values_manager.overwrite(_file_name, _criteria)