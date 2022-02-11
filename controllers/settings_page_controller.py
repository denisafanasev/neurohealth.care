import utils.ada as ada
from services.settings_service import SettingsService


class SettingsPageController():
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

    def get_assessments(self):
        page_service = SettingsService()
        assessments = page_service.get_assessments()
        assessments_list_view = []

        for assessment in assessments:
            assessments_view = {}

            assessments_view["assessment_parameters"] = assessment.assessment_parameters
            assessments_view["tests"] = assessment.tests

            assessments_list_view.append(assessments_view)

        return assessments_list_view