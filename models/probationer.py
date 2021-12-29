from datetime import datetime

class Probationer():
    """
    Класс испытуемого
    """

    def __init__(self, _probationer_id=0, _user_login="", _name_probationer="", _name_parent="",
                 _educational_institution="", _contacts="", _diagnoses="", _reasons_for_contact="", _date_of_birth=""):
        """
            Конструктор класса

            Args:
                _probationer_id(Int): id испытуемого
                _user_login(String): логин пользователя, к которому прикреплен испытуемый.
                _name_probationer(String): имя испытуемого
                _date_of_birth(date, optional): дата рождения испытуемого
                _name_parent(String): ФИО родителя испытуемого
                _educational_institution(String): учебное заведение испытуемого
                _contacts(String): контакты для связи
                _diagnoses(String): сопутствующие диагнозы
                _reasons_for_contact(String): причины обращения
        """

        self.probationer_id = _probationer_id
        self.user_login = _user_login
        self.name_probationer = _name_probationer
        if _date_of_birth != "":
            self.date_of_birth = datetime.strptime(_date_of_birth, "%Y-%m-%d").strftime("%d/%m/%Y")
        self.name_parent = _name_parent
        self.educational_institution = _educational_institution
        self.contacts = _contacts
        self.diagnoses = _diagnoses
        self.reasons_for_contact = _reasons_for_contact
