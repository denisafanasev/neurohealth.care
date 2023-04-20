import utils.ada as ada
from services.probes_service import ProbesService
from services.probationers_service import ProbationersService


class ProbesPageController():
    """
    ProbesPageController - класс контроллера представления списка проб, реализующий логику взаимодейтвия приложения с пользователем
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответсвующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """ 

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_probes(self, _user_id):
        """
        Возвращает отформатированный список тестов

        Returns:
            List: список тестов, каждый из которых представлен структурой типа Dict
        """
        probes_service = ProbesService()
        probes = []

        probes_list = probes_service.get_probes(_user_id)

        for i_probe in probes_list:
            probe = {}

            probe["probe_id"] = i_probe.probe_id
            probe["name_probationer"] = i_probe.name_probationer
            probe["probationer_id"] = i_probe.probationer_id
            probe["protocol_status"] = i_probe.protocol_status
            probe["estimated_values_file"] = i_probe.estimated_values_file
            probe["date_test"] = i_probe.date_test
            probe["date_protocol"] = i_probe.date_protocol

            probes.append(probe)

        return probes

    def is_probationers(self, _user_id):
        """
        Проверает, есть ли у пользователя тестируемые

        Returns:
            (Boolean)
        """

        probes_service = ProbesService()

        return probes_service.is_probationers(_user_id)

    def get_probes_list(self):
        """
        Возвращает список доступных проб для тестирования

        Returns:
            List(Dict): список проб
        """
        probes_service = ProbesService()

        probes_list = probes_service.get_probes_list()
        probes_list_view = []
        for probe in probes_list:
            probe_view = {
                'id': probe.id,
                'name': probe.name_probe
            }

            probes_list_view.append(probe_view)

        return probes_list_view

    def get_probationers_list(self, _user_id):
        """
        Возвращает список тестируемых текущего пользователя

        Args:
            _user_id(Int): ID текущего пользователя

        Returns:
            List(Dict): список тестируемых
        """
        probes_service = ProbesService()

        probationers_list = probes_service.get_probationers_list(_user_id)
        probationers_list_view = []
        if probationers_list is not None:
            for probationer in probationers_list:
                probationer_view = {
                    'id': probationer.probationer_id,
                    'name': probationer.name_probationer
                }

                probationers_list_view.append(probationer_view)

        return probationers_list_view
