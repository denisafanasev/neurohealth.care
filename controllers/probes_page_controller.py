import utils.ada as ada
from services.probes_service import ProbesService


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

    def get_probes(self):
        """
        Возвращает отформатированный список тестов

        Returns:
            List: список тестов, каждый из которых представлен структурой типа Dict
        """
        page_service = ProbesService()
        probes = []

        probes_list = page_service.get_probes()

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