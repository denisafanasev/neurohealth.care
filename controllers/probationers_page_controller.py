import utils.ada as ada
from services.probationers_service import ProbationersService


class ProbationersPageController():
    """
    ProbationersPageController - класс контроллера представления списка тестируемых, реализующий логику взаимодействия приложения с пользователем
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответствующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """ 

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_probationers_list_view(self):
        """
        Возвращает отформатированный список испытуемого

        Returns:
            List: список испытуемых, каждый из которых представлен структурой типа Dict
        """

        probationers_service = ProbationersService()
        probationers = probationers_service.get_probationers_list_view()

        users_list_view = []
        for probationer in probationers:

            probationer_view = {}

            probationer_view['probationer_id'] = probationer.probationer_id
            probationer_view['user_login'] = probationer.user_login
            probationer_view['name_probationer'] = probationer.name_probationer
            probationer_view['name_parent'] = probationer.name_parent
            probationer_view['date_of_birth'] = str(probationer.date_of_birth)
            probationer_view['contacts'] = probationer.contacts
            probationer_view['educational_institution'] = probationer.educational_institution

            users_list_view.append(probationer_view)

        return users_list_view
