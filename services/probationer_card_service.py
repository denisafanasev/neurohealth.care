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

    def create_probationer(self, _user_id, _probationer):
        """
        Создает в системе испытуемого

        Args:
            _user_id (String): ID пользователя, к которому прикрепиться испытуемый
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

        probationer_id, name_probationer = probationer_manager.create_probationer(_user_id, _probationer)
        login_user = user_service.get_user_by_id(_user_id).login

        action_manager.add_notifications(name_probationer, "добавил", 'нового', "probationer_manager", login_user)

        return probationer_id

    def get_probationer_card_view(self, probationer_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """

        probationer_manager = ProbationerManager()

        return probationer_manager.get_probationer_by_id(probationer_id)

    def change_probationer(self, _probationer_id, _probationer, _id_user):
        """
        Обновляет информацию о тестируемом

        Args:
            _probationer_id(Int): ID тестируемого
            _probationer(Dict): обновленные данные тестируемого
            _id_user(Int): ID текущего пользователя

        Returns:
            None
        """

        probationer_manager = ProbationerManager()
        user_manager = UserManager()
        action_manager = ActionManager()

        name_probationer = probationer_manager.change_probationer(_probationer_id, _probationer)

        login_user = user_manager.get_user_by_id(_id_user).login

        action_manager.add_notifications(name_probationer, "изменил", '', "probationer_manager", login_user)
