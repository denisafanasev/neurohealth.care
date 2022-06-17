from models.probationer_manager import ProbationerManager
from services.action_service import ActionService
from services.user_manager_service import UserManagerService

class ProbationerCardService():
    """
    ProbationerCardService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def __init__(self):
        pass

    def create_probationer(self, _user_login, _name_probationer, _date_of_birth, _name_parent,
                 _educational_institution, _contacts, _diagnoses, _reasons_for_contact):
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
        user_service = UserManagerService()

        name_probationer = probationer_manager.create_probationer( _user_login, _name_probationer, _date_of_birth,
                                               _name_parent, _educational_institution, _contacts, _diagnoses,
                                               _reasons_for_contact)
        login_user = user_service.get_current_user('').login

        ActionService().add_notifications(name_probationer, "add", 'нового', "probationer_manager", login_user)

    def get_probationer_card_view(self, probationer_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """

        probationer_manager = ProbationerManager()

        return probationer_manager.get_probationer_by_id(probationer_id)

    def change_probationer(self, _probationer_id, _name_probationer, _date_of_birth, _name_parent,
                           _educational_institution, _contacts, _diagnoses, _reasons_for_contact):
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
        user_service = UserManagerService()

        name_probationer = probationer_manager.change_probationer(_probationer_id, _name_probationer, _date_of_birth,
                            _name_parent, _educational_institution, _contacts, _diagnoses, _reasons_for_contact)

        login_user = user_service.get_current_user('').login

        ActionService().add_notifications(name_probationer, "overwrite", '', "probationer_manager", login_user)
