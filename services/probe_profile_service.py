from models.probes_manager import ProbesManager
from models.probationer_manager import ProbationerManager
from services.action_service import ActionService


class ProbeProfileService():
    """
    ProbesService - класс бизнес-логики сервиса управления пробами
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def init(self):
        pass

    def get_probationers(self):

        probationer_manager = ProbationerManager()

        return probationer_manager.get_probationers()

    def add_probe(self, _name_probationer, _probationer_id, _date_of_birth, _protocol_status):

        probes_manager = ProbesManager()

        ActionService().add_notifications(f"пробы испытуемого № {_probationer_id}", "add", "probes_manager")
        return probes_manager.add_probe(_name_probationer, _probationer_id, _date_of_birth, _protocol_status)

    def get_protocol(self, _id_test, _probe_id):

        probes_manager = ProbesManager()

        return probes_manager.get_protocol(_id_test, _probe_id)

    def get_tests_list(self):

        probes_manager = ProbesManager()

        return probes_manager.get_tests_list()

    def add_grades_in_probe(self, _grades, _probe_id, _protocol_status):

        probes_manager = ProbesManager()

        return probes_manager.add_grades_in_probe(_grades, _probe_id, _protocol_status)