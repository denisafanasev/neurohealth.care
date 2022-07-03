from models.probationer_manager import ProbationerManager
from models.user_manager import UserManager
# from services.user_manager_service import UserManagerService

class ProbationersService():
    """
    ProbationersService - класс бизнес-логики сервиса управления тестируемыми
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_probationers_list_view(self):
        """
        Возвращает список испытуемых

        Returns:
            probationers(List): список тестируемых
        """

        probationer_manager = ProbationerManager()

        probationers = probationer_manager.get_probationers()

        return probationers

    def is_probationers(self, _user_id):
        """
        Проверает, есть ли у пользователя тестируемые

        Returns:
            (Boolean): Есть/нет тестируемых
        """

        probationer_manager = ProbationerManager()
        user_manager = UserManager()
        user_login = user_manager.get_user_by_id(_user_id).login

        return probationer_manager.is_probationers(user_login)
