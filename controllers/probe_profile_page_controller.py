from services.probe_profile_service import ProbeProfileService
from services.probationer_card_service import ProbationerCardService

class ProbeProfileController():


    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_probationers(self):
        """
        Возвращает отформатированный список тестируемых

        Returns:
            List: список испытуемых, каждый из которых представлен структурой типа Dict
        """

        probe_profile_service = ProbeProfileService()
        probationers = probe_profile_service.get_probationers()

        users_list_view = []

        for probationer in probationers:
            probationer_view = {}

            probationer_view['probationer_id'] = probationer.probationer_id
            probationer_view['name_probationer'] = probationer.name_probationer
            probationer_view['date_of_birth'] = probationer.date_of_birth

            users_list_view.append(probationer_view)

        return users_list_view

    def add_probe(self, _name_probationer, _probationer_id, _date_of_birth, _protocol_status=""):
        """
        Записывает в системе только что совершенное действие авторизованного пользователя
        """

        probe_profile_service = ProbeProfileService()

        return probe_profile_service.add_probe(_name_probationer, _probationer_id, _date_of_birth, _protocol_status)

    def get_probationer_card_view(self, probationer_id):
        """
        Возвращает представление профиля тестируемого

        Returns:
            Dict: характеристики профиля пользователя
        """

        probationer_card_service = ProbationerCardService()

        return probationer_card_service.get_probationer_card_view(probationer_id)

    def get_protocol(self, _id_test, _probe_id):

        probe_profile_service = ProbeProfileService()

        try:
            protocol = probe_profile_service.get_protocol(_id_test, _probe_id)
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

        probe_profile_service = ProbeProfileService()

        return probe_profile_service.get_tests_list()

    def add_grades_in_probe(self, _grades, _probe_id, _protocol_status=""):

        probe_profile_service = ProbeProfileService()

        return probe_profile_service.add_grades_in_probe(_grades, _probe_id, _protocol_status)
