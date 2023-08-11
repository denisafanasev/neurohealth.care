from flask_babel import gettext

import config
from services.probationer_card_service import ProbationerCardService

class ProbationerCardPageController():

    def __init__(self):
        pass

    def create_probationers(self, _user_id, _probationer):
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

        return probationer_card_service.create_probationer( _user_id, _probationer)

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

        patient_view_placeholder = {
            "name_probationer": gettext("введите имя испытуемого.."),
            "date_of_birth": gettext("введите дату рождения.."),
            "name_parent": gettext("введите ФИО родителя.."),
            "contacts": gettext("введите контакты для связи.."),
            "educational_institution": gettext("введите название учебного заведения.."),
            "diagnoses": gettext("введите диагнозы.."),
            "reasons_for_contact": gettext("введите причины обращения..")
        }

        return patient_view, patient_view_placeholder

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

        probationer_card_service = ProbationerCardService()

        return probationer_card_service.change_probationer(int(_probationer_id), _probationer, _id_user)

    def get_settings_probationer(self):
        """
        Возвращает возможные настройки тестируемого
        """

        settings = {"educational_institution": config.EDUCATIONAL_INSTITUSION}

        return settings


