import utils.ada as ada
from services.probes_service import ProtocolsService
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
        probes_service = ProtocolsService()

        probes_list = probes_service.get_probes(_user_id)
        probes_list_view = []
        for probe in probes_list:
            probe_view = {}

            probe_view["probe_id"] = probe.probe_id
            probe_view["name_probationer"] = probe.name_probationer
            probe_view["probationer_id"] = probe.probationer_id
            probe_view["protocol_status"] = probe.protocol_status
            probe_view["estimated_values_file"] = probe.estimated_values_file
            probe_view["date_test"] = probe.date_test
            probe_view["date_protocol"] = probe.date_protocol
            probe_view['test'] = probe.test.name_probe

            probes_list_view.append(probe_view)

        return probes_list_view

    def is_probationers(self, _user_id):
        """
        Проверает, есть ли у пользователя тестируемые

        Returns:
            (Boolean)
        """

        probes_service = ProtocolsService()

        return probes_service.is_probationers(_user_id)

    def get_probes_list(self):
        """
        Возвращает список доступных проб для тестирования

        Returns:
            List(Dict): список проб
        """
        probes_service = ProtocolsService()

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
        probes_service = ProtocolsService()

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
    
    def add_protocol(self, _probationer_id, _probe_id, _user_id):
        
        protocols_service = ProtocolsService()

        return protocols_service.add_protocol(_probationer_id, _probe_id, _user_id)