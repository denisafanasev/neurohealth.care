from models.probes_manager import ProbesManager
from models.probationer_manager import ProbationerManager
from models.user_manager import UserManager


class ProbesService():
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
        probes_manager = ProbesManager()
        probationer_manager = ProbationerManager()

        user = user_manager.get_user_by_id(_user_id)
        probationers_list = probationer_manager.get_probationers(user)
        probes_list = []
        for probationer in probationers_list:
            probes = probes_manager.get_probes_by_probationer_id(probationer.probationer_id)
            if probes:
                probes_list.extend(probes)

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

        probes_manager = ProbesManager()

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

