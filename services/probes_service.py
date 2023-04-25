from models.action_manager import ActionManager
from models.probes_manager import ProtocolsManager
from models.probationer_manager import ProbationerManager
from models.user_manager import UserManager


class ProtocolsService():
    """
    ProbesService - класс бизнес-логики сервиса управления пробами
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_probes(self, _user_id):
        """
        Возвращает список проб

        Returns:
            List: список проб
        """
        user_manager = UserManager()
        probes_manager = ProtocolsManager()
        probationer_manager = ProbationerManager()

        user = user_manager.get_user_by_id(_user_id)
        probationers_list = probationer_manager.get_probationers(user)
        probes_list = []
        for probationer in probationers_list:
            probes = probes_manager.get_probes_by_probationer_id(probationer.probationer_id)
            if probes:
                probes_probationer_list = []
                for probe in probes:
                    probe.test = probes_manager.get_probe_by_id_grade(probe.test)
                    probes_probationer_list.append(probe)

                probes_list.extend(probes_probationer_list)

        return probes_list

    def is_probationers(self, _user_id):
        """
        Проверает, есть ли у пользователя тестируемые

        Returns:
            (Boolean): Есть/нет тестируемых
        """

        probationer_manager = ProbationerManager()
        # user_manager = UserManager()
        # user_login = user_manager.get_user_by_id(_user_id).login

        return probationer_manager.is_probationers(_user_id)

    def get_probes_list(self):
        """
        Возвращает список доступных проб для тестирования

        Returns:
            List(Probe): список проб
        """

        probes_manager = ProtocolsManager()

        return probes_manager.get_probes_list()

    def get_probationers_list(self, _user_id):
        """
        Возвращает список тестируемых текущего пользователя

        Args:
            _user_id(Int): ID текущего пользователя

        Returns:
            List(User): список тестируемых
        """
        user_manager = UserManager()
        probationer_manager = ProbationerManager()

        user = user_manager.get_user_by_id(_user_id)
        return probationer_manager.get_probationers(user)

    def add_protocol(self, _probationer_id, _probe_id, _user_id):
        """
        Добавляет в базу данных пробу тестируемого

        Args:
            _name_probationer(String): имя тестируемого
            _probationer_id(Int): индентификатор тестируемого
            _date_of_birth(String): дата рождения тестируемого
            _protocol_status(String): статус пробы
        """

        probes_manager = ProtocolsManager()
        user_manager = UserManager()
        action_manager = ActionManager()

        protocol_id = probes_manager.add_protocol(_probationer_id, _probe_id)
        login_user = user_manager.get_user_by_id(_user_id).login

        action_manager.add_notifications(f"пробы испытуемого № {_probationer_id}", "добавил", '', "probes_manager",
                                         login_user)
        return protocol_id

