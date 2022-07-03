from models.estimated_values_manager import EstimatedValuesManager
from models.user_manager import UserManager
from models.action_manager import ActionManager


class EstimatedValuesService():
    """
    EstimatedValuesService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass


    def get_assessments(self, _id_file_name):
        """
        Возвращает оценочные значения для тестов

        Args:
            _id_file_name(Int): индентификатор названия файла с тестами

        Returns:
            EstimatedValues: оценочные значения
        """

        estimated_values_manager = EstimatedValuesManager()

        return estimated_values_manager.get_assessments(_id_file_name)

    def get_age_ranges(self):
        """
        Возвращает список диапазонов возрастов

        Returns:
            List: список диапазонов возрастов
        """
        estimated_values_manager = EstimatedValuesManager()

        return estimated_values_manager.get_age_ranges()

    def overwrite(self, _id_file_name, _criteria, _id_user):
        """
        Изменяет оценочные значения в тестах

        Args:
            _id_file_name(Int): индентификатор названия файла с тестами
            _criteria(Dict): словарь с измененными оценочными значениями
        """

        estimated_values_manager = EstimatedValuesManager()
        user_manager = UserManager()
        action_manager = ActionManager()

        file_name = estimated_values_manager.overwrite(_id_file_name, _criteria)
        login_user = user_manager.get_user_by_id(_id_user).login

        action_manager.add_notifications(file_name, "overwrite", '', "estimated_values", login_user)
