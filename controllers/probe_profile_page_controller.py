from services.probe_profile_service import ProbeProfileService


class ProbeProfileController():


    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_probationers(self):
        """
        Возвращает отформатированный список испытуемого

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
            probationer_view['date_of_birth'] = str(probationer.date_of_birth.strftime("%d/%m/%Y"))

            users_list_view.append(probationer_view)

        return users_list_view

    def add_probe(self, _probationer, _protocol_status):

        probe_profile_service = ProbeProfileService()

        return probe_profile_service.add_probe(_probationer, _protocol_status)
