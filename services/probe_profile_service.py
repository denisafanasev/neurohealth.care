from models.probes_manager import ProbesManager
from models.probationer_manager import ProbationerManager


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

    def add_probe(self, _probationer, _protocol_status):

        probes_manager = ProbesManager()

        return probes_manager.add_probe(_probationer, _protocol_status)