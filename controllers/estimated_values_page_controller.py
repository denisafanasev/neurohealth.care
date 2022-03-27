import utils.ada as ada
from services.estimated_values_service import EstimatedValuesService


class EstimatedValuesPageController():
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

    def get_assessments(self, _file_name="базовые значение"):

        page_service = EstimatedValuesService()
        assessments = page_service.get_assessments(_file_name)
        assessments_list_view = []

        for assessment in assessments:
            assessments_view = {}

            assessments_view["id"] = assessment.id
            assessments_view["assessment_parameters"] = assessment.assessment_parameters
            assessments_view["tests"] = assessment.tests

            assessments_list_view.append(assessments_view)

        return assessments_list_view

    def get_age_ranges(self):

        page_service = EstimatedValuesService()

        return page_service.get_age_ranges()

    def overwrite(self, _file_name, _criteria):

        page_service = EstimatedValuesService()

        return page_service.overwrite(_file_name, _criteria)
