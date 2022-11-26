from models.education_stream import EducationStream
from data_adapters.data_store import DataStore
from datetime import datetime, timedelta


class EducationStreamManager():
    """
    Менеджер управления обучающими потоками
    """

    def education_stream_row_to_education_stream(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о пользователи в структуру EducationStream

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            EducationStream: обучающий поток
        """

        education_stream = EducationStream(_id=_data_row.doc_id, _name=_data_row['name'], _id_course=_data_row['id_course'],
                                         _curators_list=_data_row['curators_list'], _students_list=_data_row['students_list'],
                                         _teacher=_data_row['teacher'])

        if _data_row.get('date_start') is not None:
            if type(_data_row.get('date_start')) is str:
                education_stream.date_start = datetime.strptime(_data_row.get('date_start'), '%d/%m/%Y')
            else:
                education_stream.date_start = _data_row.get('date_start')
        else:
            education_stream.date_start = datetime.today()

        if _data_row.get('date_end') is not None:
            if type(_data_row.get('date_end')) is str:
                education_stream.date_end = datetime.strptime(_data_row.get('date_end'), '%d/%m/%Y')
            else:
                education_stream.date_end = _data_row.get('date_end')
        else:
            education_stream.date_end = datetime.today() + timedelta(days=1)

        if datetime.today() <= education_stream.date_end + timedelta(days=1):
            if datetime.today() >= education_stream.date_start:
                education_stream.status = "идет"
            else:
                education_stream.status = "запланирован"
        else:
            education_stream.status = "закончен"

        return education_stream

    def create_education_stream(self, _education_stream):
        """
        Создает обучающий поток

        Args:
            _education_stream(Dict): обучающий поток
        """

        data_store = DataStore("education_streams")

        id_education_stream = data_store.insert_row({'name': _education_stream['name'], 'date_start': _education_stream['date_start'],
                               "date_end": _education_stream['date_end'], "teacher": _education_stream['teacher'],
                               "id_course": _education_stream['id_course'],
                               "curators_list": _education_stream['curators_list'],
                               "students_list": _education_stream['students_list']})

        return id_education_stream

    def get_education_streams(self):
        """
        Возвращает список обучающих потоков

        Returns:
            education_streams_list(List): список обучающих потоков
        """

        data_store = DataStore('education_streams')

        education_streams = data_store.get_rows()

        education_streams_list = []

        for i_education_stream in education_streams:
            education_streams_list.append(self.education_stream_row_to_education_stream(i_education_stream))

        return education_streams_list

    def get_education_stream(self, _id):
        """
        Возвращает обучающий поток по id

        Args:
            _id(Int): идентификатор обучающего потока
        """

        data_store = DataStore('education_streams')

        education_stream = data_store.get_row_by_id(_id)

        if education_stream != []:

            return self.education_stream_row_to_education_stream(education_stream)
        else:
            return None

    def save_education_stream(self, _education_stream):
        """
        Изменяет данные обучающего потока

        Args:
            _education_stream(Dict): обучающий поток
        """

        data_store = DataStore('education_streams')

        # создаем объект обучающего потока, чтобы отработать в нем логику установки атрибутов
        education_stream = EducationStream(_id=_education_stream['id'], _name=_education_stream['name'], _id_course=_education_stream['id_course'],
                                         _curators_list=_education_stream['curators_list'], _students_list=_education_stream['students_list'],
                                         _teacher=_education_stream['teacher'], _date_start=_education_stream['date_start'], _date_end=_education_stream['date_end'])

        # сохранение проводим из атрибутов объекта обучающего потока
        data_store.update_row_by_id({"name": education_stream.name,
                               'date_start': education_stream.date_start.strftime('%d/%m/%Y'),
                               "date_end": education_stream.date_end.strftime('%d/%m/%Y'), "teacher": education_stream.teacher,
                               "id_course": education_stream.course, "curators_list": education_stream.curators_list,
                               "students_list": education_stream.students_list}, education_stream.id)

        return education_stream

    def get_education_streams_list_by_id_user(self, _id_user, _role_user):
        """
        Возвращает список обучающих потоков, в которых находится данный пользователь

        Args:
            _id_user(Int): ID пользователя
            _role_user(String): роль пользователя

        Returns:
            List(EducationStream): список обучающих потоков
        """
        data_store = DataStore("education_streams")

        education_streams_list = data_store.get_rows()
        education_streams = []
        for i_education_stream in education_streams_list:
            education_stream = self.education_stream_row_to_education_stream(i_education_stream)
            if _role_user == "user":
                if _id_user in education_stream.students_list:
                    education_streams.append(education_stream)
            elif _role_user == "superuser":
                if _id_user in education_stream.curators_list:
                    education_streams.append(education_stream)

        return education_streams

    def get_education_stream_by_id_user_and_id_course(self, _id_user, _id_course):
        """
        Возвращает список обучающих потоков, в которых находится данный пользователь

        Args:
            _id_user(Int): ID пользователя
            _id_course(Int): ID курса

        Returns:
            EducationStream: обучающий поток
        """
        data_store = DataStore("education_streams")

        education_streams_list = data_store.get_rows({'id_course': _id_course})
        for i_education_stream in education_streams_list:
            education_stream = self.education_stream_row_to_education_stream(i_education_stream)
            if education_stream.status == 'идет':
                if _id_user in education_stream.students_list:
                    return education_stream

