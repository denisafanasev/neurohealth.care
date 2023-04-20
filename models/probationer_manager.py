from data_adapters.data_store import DataStore
from models.probationer import Probationer
from datetime import datetime
from error import ProbationerManagerException


class ProbationerManager():

    def probationer_row_to_probationer(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о тестируемом в структуру Probationer

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Probationer: испытуемый
        """

        # создадим пользователя с указанием обязательных атрибутов
        probationer = Probationer(_data_row.doc_id, _name_probationer=_data_row['name_probationer'],
                                  _name_parent=_data_row['name_parent'],
                                  _educational_institution=_data_row['educational_institution'],
                                  _contacts=_data_row['contacts'], _diagnoses=_data_row['diagnoses'],
                                  _reasons_for_contact=_data_row['reasons_for_contact'],
                                  _user_id=_data_row['user_id'])

        # проверим наличие в структуре хранения необязательных атрибутов

        return probationer

    def get_probationer_by_id(self, _probationer_id):
        """
        Возвращает объект Probationer по id испытуемого

        Args:
            _probationers_id   - Required  : id пользователя (Int)
        """

        data_store = DataStore("probationers")

        patient = None

        patients_data = data_store.get_row_by_id(_probationer_id)

        if patients_data is not None:
            patient = self.probationer_row_to_probationer(patients_data)

            patient.date_of_birth = datetime.strptime(patients_data["date_of_birth"], "%d/%m/%Y").strftime("%Y-%m-%d")

        return patient

    def get_probationers(self, _user):
        """
        Возвращает список испытуемых

        Args:
            _user(User): пользователь

        Returns:
            probationers(List): список тестируемых
        """
        probationers = []

        data_store = DataStore("probationers")

        patients_list_data = data_store.get_rows()

        for patients_data in patients_list_data:

            patient = self.probationer_row_to_probationer(patients_data)

            patient.date_of_birth = datetime.strptime(patients_data["date_of_birth"], "%d/%m/%Y").strftime("%d/%m/%Y")

            if _user.role == "superuser":
                probationers.append(patient)
            elif patient.user_id == _user.user_id:
                probationers.append(patient)

        return probationers

    def create_probationer(self, _user_id, _name_probationer, _date_of_birth, _name_parent,
                           _educational_institution, _contacts, _diagnoses, _reasons_for_contact):
        """
        Процедура создания нового испытуемого в системе

        Args:
            _user_login(String): логин пользователя, к которому прикреплен испытуемый.
            _name_probationer(String): имя испытуемого
            _date_of_birth(date, optional): дата рождения испытуемого
            _name_parent(String): ФИО родителя испытуемого
            _educational_institution(String): учебное заведение испытуемого
            _contacts(String): контакты для связи
            _diagnoses(String): сопутствующие диагнозы
            _reasons_for_contact(String): причины обращения
        """

        # создаем новую запись
        data_store = DataStore("probationers")

        # создаем новую запись
        probationer = Probationer(_user_id=_user_id, _name_probationer=_name_probationer,
                                  _name_parent=_name_parent, _educational_institution=_educational_institution,
                                  _contacts=_contacts, _diagnoses=_diagnoses, _reasons_for_contact=_reasons_for_contact)

        probationer.date_of_birth = datetime.strptime(_date_of_birth, "%Y-%m-%d").strftime("%d/%m/%Y")

        probationer_data = {"user_login": probationer.user_id, "name_probationer": probationer.name_probationer,
                            "date_of_birth": probationer.date_of_birth, "name_parent": probationer.name_parent,
                            "educational_institution": probationer.educational_institution,
                            "contacts": probationer.contacts, "diagnoses": probationer.diagnoses,
                            "reasons_for_contact": probationer.reasons_for_contact}

        data_store.insert_row(probationer_data)

        return probationer.name_probationer

    def change_probationer(self, _probationer_id, _name_probationer, _date_of_birth, _name_parent,
                           _educational_institution,
                           _contacts, _diagnoses, _reasons_for_contact):
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

        probationer = Probationer(_probationer_id=_probationer_id, _name_probationer=_name_probationer,
                                  _name_parent=_name_parent, _educational_institution=_educational_institution,
                                  _contacts=_contacts, _diagnoses=_diagnoses, _reasons_for_contact=_reasons_for_contact)

        probationer.date_of_birth = datetime.strptime(_date_of_birth, "%Y-%m-%d").strftime("%d/%m/%Y")

        probationer_data = {"name_probationer": probationer.name_probationer,
                            "date_of_birth": probationer.date_of_birth, "name_parent": probationer.name_parent,
                            "educational_institution": probationer.educational_institution,
                            "contacts": probationer.contacts, "diagnoses": probationer.diagnoses,
                            "reasons_for_contact": probationer.reasons_for_contact}

        data = DataStore("probationers")

        data.update_row_by_id(probationer_data, probationer.probationer_id)

        return probationer.name_probationer

    def is_probationers(self, _user_id):

        data_store = DataStore("probationers")

        if data_store.get_rows({"user_id": _user_id}) != []:
            return True
        else:
            return False
