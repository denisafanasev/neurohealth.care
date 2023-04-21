from models.probationer_manager import ProbationerManager
from models.user_manager import UserManager

class ProbationersService():
    """
    ProbationersService - класс бизнес-логики сервиса управления тестируемыми
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_probationers_list_view(self, _user_id):
        """
        Возвращает список испытуемых

        Returns:
            probationers(List): список тестируемых
        """

        probationer_manager = ProbationerManager()
        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)

        probationers = probationer_manager.get_probationers(user)

        return probationers

    def get_user_by_id(self, _user_id):
        """
        Возвращает пользователя по ID

        Args:
            _user_id(Int): ID

        Returns:
            User: пользователя
        """
        user_manager = UserManager()

        return user_manager.get_user_by_id(_user_id)
