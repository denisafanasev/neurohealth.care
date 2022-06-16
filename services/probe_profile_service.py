from models.probes_manager import ProbesManager
from models.probationer_manager import ProbationerManager
from services.action_service import ActionService
from services.user_manager_service import UserManagerService


class ProbeProfileService():
    """
    ProbesService - класс бизнес-логики сервиса управления пробами
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def init(self):
        pass

    def get_probationers(self):
        """
        Возвращает список тестируемых

        Returns:
            (List): список тестируемых
        """

        probationer_manager = ProbationerManager()

        return probationer_manager.get_probationers()

    def add_probe(self, _name_probationer, _probationer_id, _date_of_birth, _protocol_status):
        """
        Добавляет в базу данных пробу тестируемого

        Args:
            _name_probationer(String): имя тестируемого
            _probationer_id(Int): индентификатор тестируемого
            _date_of_birth(String): дата рождения тестируемого
            _protocol_status(String): статус пробы
        """

        probes_manager = ProbesManager()
        user_service = UserManagerService()

        probe_id = probes_manager.add_probe(_name_probationer, _probationer_id, _date_of_birth, _protocol_status)
        login_user = user_service.get_current_user('').login

        ActionService().add_notifications(f"пробы испытуемого № {_probationer_id}", "add", '', "probes_manager",
                                          login_user)
        return probe_id

    def get_protocol(self, _id_test, _probe_id):
        """
        Возвращает тест из пробы тестируемого

        Args:
            _id_test(Int): индентификатор теста
            _probe_id(Int): индентафикатор пробы

        Return:
            Тест из пробы
        """

        probes_manager = ProbesManager()

        return probes_manager.get_protocol(_id_test, _probe_id)

    def get_tests_list(self):
        """
        Возвращает список тестов

        Returns:
            Список тестов
        """

        probes_manager = ProbesManager()

        return probes_manager.get_tests_list()

    def add_grades_in_probe(self, _grades, _probe_id, _protocol_status):
        """
        Добавление оценок за тест тестируемого в базу данных

        Args:
            _grades(List):список оценок за тест
            _probe_id(Int): индентификатор пробы
            _protocol_status(String): статус пробы
        """

        probes_manager = ProbesManager()

        return probes_manager.add_grades_in_probe(_grades, _probe_id, _protocol_status)