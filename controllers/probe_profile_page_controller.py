from services.probe_profile_service import ProbeProfileService
from services.probationer_card_service import ProbationerCardService

class ProbeProfileController():


    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_probationers(self, _user_id):
        """
        Возвращает отформатированный список тестируемых

        Returns:
            List: список испытуемых, каждый из которых представлен структурой типа Dict
        """

        probe_profile_service = ProbeProfileService()
        probationers = probe_profile_service.get_probationers(_user_id)

        users_list_view = []

        for probationer in probationers:
            probationer_view = {}

            probationer_view['probationer_id'] = probationer.probationer_id
            probationer_view['name_probationer'] = probationer.name_probationer
            probationer_view['date_of_birth'] = probationer.date_of_birth

            users_list_view.append(probationer_view)

        return users_list_view

    def add_probe(self, _name_probationer, _probationer_id, _date_of_birth, _id_user,_protocol_status=""):
        """
        Записывает в системе только что совершенное действие авторизованного пользователя
        """

        probe_profile_service = ProbeProfileService()

        return probe_profile_service.add_probe(_name_probationer, _probationer_id, _date_of_birth, _protocol_status, _id_user)

    def get_probationer_card_view(self, probationer_id):
        """
        Возвращает представление профиля тестируемого

        Returns:
            Dict: характеристики профиля пользователя
        """

        probationer_card_service = ProbationerCardService()

        return probationer_card_service.get_probationer_card_view(probationer_id)

    def get_protocol(self, _probationer_id, _probe_id):
        """
        Возвращает тест из пробы тестируемого

        Args:
            _id_test(Int): индентификатор теста
            _probe_id(Int): индентафикатор пробы

        Return:
            Тест из пробы
        """

        probe_profile_service = ProbeProfileService()

        try:
            protocol = probe_profile_service.get_protocol(_probationer_id, _probe_id)
            probe = {}

            probe["id"] = protocol.test.id
            probe["name_probe"] = protocol.test.name_probe
            probe["parameters"] = protocol.test.parameters
            probe["name_probationer"] = protocol.name_probationer
            probe["protocol_status"] = protocol.protocol_status
        except AttributeError:
            return None

        return probe

    def get_tests_list(self):
        """
        Возвращает список тестов

        Returns:
            Список тестов
        """

        probe_profile_service = ProbeProfileService()

        return probe_profile_service.get_tests_list()

    def add_grades_in_probe(self, _grades, _probe_id, _protocol_status=""):
        """
        Добавление оценок за тест тестируемого в базу данных

        Args:
            _grades(List):список оценок за тест
            _probe_id(Int): индентификатор пробы
            _protocol_status(String): статус пробы
        """

        probe_profile_service = ProbeProfileService()

        return probe_profile_service.add_grades_in_probe(_grades, _probe_id, _protocol_status)
