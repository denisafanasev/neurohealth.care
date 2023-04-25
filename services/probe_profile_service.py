from models.probes_manager import ProtocolsManager
from models.probationer_manager import ProbationerManager
from models.action_manager import ActionManager
from models.user_manager import UserManager


class ProbeProfileService():
    """
    ProbesService - класс бизнес-логики сервиса управления пробами
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def init(self):
        pass

    def get_probationers(self, _user_id):
        """
        Возвращает список тестируемых

        Returns:
            (List): список тестируемых
        """

        probationer_manager = ProbationerManager()
        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)

        return probationer_manager.get_probationers(user)

    def update_protocol(self, _probationer_id, _protocol_status, _id_user):
        """
        Добавляет в базу данных пробу тестируемого

        Args:
            _name_probationer(String): имя тестируемого
            _probationer_id(Int): индентификатор тестируемого
            _date_of_birth(String): дата рождения тестируемого
            _protocol_status(String): статус пробы
        """

        protocols_manager = ProtocolsManager()
        user_manager = UserManager()
        action_manager = ActionManager()

        protocol_id = protocols_manager.add_protocol(_probationer_id, _protocol_status)
        login_user = user_manager.get_user_by_id(_id_user).login

        action_manager.add_notifications(f"пробы испытуемого № {_probationer_id}", "добавил", '', "probes_manager",
                                          login_user)
        return protocol_id

    def get_protocol(self, _protocol_id):
        """
        Возвращает тест из пробы тестируемого

        Args:
            _id_test(Int): идентификатор теста
            _probe_id(Int): идентификатор пробы

        Return:
            Тест из пробы
        """

        protocols_manager = ProtocolsManager()
        protocol = protocols_manager.get_protocol_by_id(_protocol_id)
        # probe_id = protocol.test.split('_')[-1]
        return protocols_manager.get_protocol(_protocol_id)

    def get_tests_list(self):
        """
        Возвращает список тестов

        Returns:
            Список тестов
        """

        protocols_manager = ProtocolsManager()

        return protocols_manager.get_tests_list()

    def add_grades_in_probe(self, _grades, _probe_id, _protocol_status):
        """
        Добавление оценок за тест тестируемого в базу данных

        Args:
            _grades(List):список оценок за тест
            _probe_id(Int): индентификатор пробы
            _protocol_status(String): статус пробы
        """

        protocols_manager = ProtocolsManager()

        return protocols_manager.add_grades_in_probe(_grades, _probe_id, _protocol_status)