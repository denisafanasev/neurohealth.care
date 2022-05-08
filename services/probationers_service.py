from models.probationer_manager import ProbationerManager

class ProbationersService():
    """
    ProbationersService - класс бизнес-логики сервиса управления тестируемыми
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_probationers_list_view(self):

         probationers = []
         probationer_manager = ProbationerManager()

         probationers = probationer_manager.get_probationers()

         return probationers

    def is_probationers(self):

        probationer_manager = ProbationerManager()

        return probationer_manager.is_probationers()