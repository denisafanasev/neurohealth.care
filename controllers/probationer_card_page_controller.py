import config
from services.probationer_card_service import ProbationerCardService

class ProbationerCardPageController():

    def __init__(self):
        pass

    def create_probationers(self, _user_login, _name_probationer, _date_of_birth, _name_parent,
                            _educational_institution, _contacts, _diagnoses, _reasons_for_contact):
        """
        Создает в системе тестируемого

        Args:
            _user_login (String): логин пользователя, к которому прикрепиться тестируемый
            _name_probationer (String): имя тестируемого
            _date_of_birth (String): дата рождения тестируемого
            _name_parent (String): ФИО родителя тестируемого
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
        Возвращает представление профиля тестируемого

        Returns:
            Dict: характеристики профиля пользователя
        """

        probationer_card_service = ProbationerCardService()

        patient = probationer_card_service.get_probationer_card_view(probationer_id)

        patient_view = {}
        if patient is not None:
            patient_view["name_probationer"] = patient.name_probationer
            patient_view["date_of_birth"] = patient.date_of_birth
            patient_view["name_parent"] = patient.name_parent
            patient_view["contacts"] = patient.contacts
            patient_view["educational_institution"] = patient.educational_institution
            patient_view["diagnoses"] = patient.diagnoses
            patient_view["reasons_for_contact"] = patient.reasons_for_contact
        else:
            patient_view["name_probationer"] = "введите имя испытуемого.."
            patient_view["date_of_birth"] = "введите дату рождения.."
            patient_view["name_parent"] = "введите ФИО родителя.."
            patient_view["contacts"] = "введите контакты для связи.."
            patient_view["educational_institution"] = "введите название учебного заведения.."
            patient_view["diagnoses"] = "введите диагнозы.."
            patient_view["reasons_for_contact"] = "введите причины обращения.."

        return patient_view

    def change_probationer(self, _probationer_id, _name_probationer, _date_of_birth, _name_parent,
                           _educational_institution,
                           _contacts, _diagnoses, _reasons_for_contact):
        """
        Обновляет информацию о тестируемом

        Returns:
        """

        probationer_card_service = ProbationerCardService()

        return probationer_card_service.change_probationer(_probationer_id, _name_probationer, _date_of_birth, _name_parent,
                           _educational_institution,
                           _contacts, _diagnoses, _reasons_for_contact)

    def get_settings_probationer(self):
        """
        Возвращает возможные настройки тестируемого
        """

        settings = {}

        settings["educational_institution"] = config.EDUCATIONAL_INSTITUSION

        return settings


