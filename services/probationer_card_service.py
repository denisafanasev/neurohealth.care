from models.probationer_manager import ProbationerManager
from models.action_manager import ActionManager
from models.user_manager import UserManager


class ProbationerCardService():
    """
    ProbationerCardService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def __init__(self):
        pass

    def create_probationer(self, _user_login, _name_probationer, _date_of_birth, _name_parent,
                 _educational_institution, _contacts, _diagnoses, _reasons_for_contact, _id_user):
        """
        Создает в системе испытуемого

        Args:
            _user_login (String): логин пользователя, к которому прикрепиться испытуемый
            _name_probationer (String): имя испытуемого
            _date_of_birth (String): дата рождения испытуемого
            _name_parent (String): ФИО родителя испытуемого
            _educational_institution (String): учебное заведение
            _contacts (String): контакты
            _diagnoses (String): сопутствующие диагнозы
            _reasons_for_contact (String): причины обращения
        """

        probationer_manager = ProbationerManager()
        user_service = UserManager()
        action_manager = ActionManager()

        name_probationer = probationer_manager.create_probationer( _user_login, _name_probationer, _date_of_birth,
                                               _name_parent, _educational_institution, _contacts, _diagnoses,
                                               _reasons_for_contact)
        user = user_service.get_user_by_id(_id_user)

        action_manager.add_notifications(name_probationer, "добавил", 'нового', "probationer_manager", user)

    def get_probationer_card_view(self, probationer_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """

        probationer_manager = ProbationerManager()

        return probationer_manager.get_probationer_by_id(probationer_id)

    def change_probationer(self, _probationer_id, _name_probationer, _date_of_birth, _name_parent,
                           _educational_institution, _contacts, _diagnoses, _reasons_for_contact, _id_user):
        """
        Записывает изменения данных тестируемого

        Args:
            _probationer_id(Int): id тестируемого
            _name_probationer(String): имя тестируемого
            _date_of_birth(date, optional): дата рождения тестируемого
            _name_parent(String): ФИО родителя тестируемого
            _educational_institution(String): учебное заведение тестируемого
            _contacts(String): контакты для связи
            _diagnoses(String): сопутствующие диагнозы
            _reasons_for_contact(String): причины обращения
        """

        probationer_manager = ProbationerManager()
        user_manager = UserManager()
        action_manager = ActionManager()

        name_probationer = probationer_manager.change_probationer(_probationer_id, _name_probationer, _date_of_birth,
                            _name_parent, _educational_institution, _contacts, _diagnoses, _reasons_for_contact)

        user = user_manager.get_user_by_id(_id_user)

        action_manager.add_notifications(name_probationer, "изменил", '', "probationer_manager", user)
