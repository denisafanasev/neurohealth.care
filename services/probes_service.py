from models.probes_manager import ProbesManager


class ProbesService():
    """
    ProbesService - класс бизнес-логики сервиса управления пробами
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_probes(self):

        probes_manager = ProbesManager()

        return probes_manager.get_probes()
