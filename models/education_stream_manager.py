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

        education_stream = EducationStream(_id=_data_row['id'], _name=_data_row['name'], _id_course=_data_row['id_course'],
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

        rows = data_store.get_rows()
        _education_stream['id'] = max([i['id'] for i in rows]) + 1
        education_stream = self.education_stream_row_to_education_stream(_education_stream)

        data_store.add_row({'id': education_stream.id, 'name': education_stream.name,
                            'date_start': education_stream.date_start.strftime('%d/%m/%Y'),
                            "date_end": education_stream.date_end.strftime('%d/%m/%Y'), "teacher": education_stream.teacher,
                            "id_course": education_stream.course, "curators_list": education_stream.curators_list,
                            "students_list": education_stream.students_list})

        return education_stream

    def get_education_streams_list(self):
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

        education_stream = data_store.get_rows({"id": _id})

        if education_stream != []:

            return self.education_stream_row_to_education_stream(education_stream[0])
        else:
            return None

    def change_education_stream(self, _education_stream):
        """
        Изменяет данные обучающего потока

        Args:
            _education_stream(Dict): обучающий поток
        """

        data_store = DataStore('education_streams')

        education_stream = self.education_stream_row_to_education_stream(_education_stream)

        data_store.update_row({'id': education_stream.id, "name": education_stream.name,
                               'date_start': education_stream.date_start.strftime('%d/%m/%Y'),
                               "date_end": education_stream.date_end.strftime('%d/%m/%Y'), "teacher": education_stream.teacher,
                               "id_course": education_stream.course, "curators_list": education_stream.curators_list,
                               "students_list": education_stream.students_list}, 'id')

        return education_stream

    def get_education_streams_list_by_login_user(self, _login_user, _role_user):

        data_store = DataStore("education_streams")

        education_streams_list = data_store.get_rows()
        education_streams = []
        for i_education_stream in education_streams_list:
            education_stream = self.education_stream_row_to_education_stream(i_education_stream)
            if _role_user == "user":
                if _login_user in education_stream.students_list:
                    education_streams.append(education_stream)
            elif _role_user == "superuser":
                if _login_user in education_stream.curators_list:
                    education_streams.append(education_stream)

        return education_streams
