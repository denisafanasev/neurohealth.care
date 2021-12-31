from services.probationer_card_service import ProbationerCardService

class ProbationerCardPageController():

    def __init__(self):
        pass

    def create_probationers(self, _user_login, _name_probationer, _date_of_birth, _name_parent,
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

        probationer_card_service = ProbationerCardService()

        probationer_card_service.create_probationer( _user_login, _name_probationer, _date_of_birth,
                                                    _name_parent, _educational_institution, _contacts, _diagnoses,
                                                    _reasons_for_contact)

    def get_probationer_card_view(self, probationer_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """

        probationer_card_service = ProbationerCardService()

        return probationer_card_service.get_probationer_card_view(probationer_id)



