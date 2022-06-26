from models.learning_stream import LearningStream
from data_adapters.data_store import DataStore
from datetime import datetime, timedelta


class LearningStreamManager():

    def learning_stream_row_to_learning_stream(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о пользователи в структуру LearningStream

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            LearningStream: обучающий поток
        """

        learning_stream = LearningStream(_id=_data_row['id'], _name=_data_row['name'], _id_course=_data_row['id_course'],
                                         _curators_list=_data_row['curators_list'], _students_list=_data_row['students_list'],
                                         _teacher=_data_row['teacher'])

        if _data_row.get('date_start') is not None:
            if type(_data_row.get('date_start')) is str:
                learning_stream.date_start = datetime.strptime(_data_row.get('date_start'), '%d/%m/%Y')
            else:
                learning_stream.date_start = _data_row.get('date_start')
        else:
            learning_stream.date_start = datetime.today()

        if _data_row.get('date_end') is not None:
            if type(_data_row.get('date_end')) is str:
                learning_stream.date_end = datetime.strptime(_data_row.get('date_end'), '%d/%m/%Y')
            else:
                learning_stream.date_end = _data_row.get('date_end')
        else:
            learning_stream.date_end = datetime.today() + timedelta(days=1)

        if _data_row.get('status') is not None:
            learning_stream.status = _data_row.get('status')
        else:
            if datetime.now() <= learning_stream.date_end:
                if datetime.now() >= learning_stream.date_start:
                    learning_stream.status = "идет"
                else:
                    learning_stream.status = "запланирован"
            else:
                learning_stream.status = "закончен"

        return learning_stream

    def create_learning_stream(self, _learning_stream):
        """
        Создает обучающий поток

        Args:
            _learning_stream(Dict): обучающий поток
        """

        data_store = DataStore("learning_streams")

        rows = data_store.get_rows()
        _learning_stream['id'] = max([i['id'] for i in rows]) + 1
        learning_stream = self.learning_stream_row_to_learning_stream(_learning_stream)

        data_store.add_row({'id': learning_stream.id, 'name': learning_stream.name,
                            'date_start': learning_stream.date_start.strftime('%d/%m/%Y'),
                            "date_end": learning_stream.date_end.strftime('%d/%m/%Y'), "teacher": learning_stream.teacher,
                            "id_course": learning_stream.course, "curators_list": learning_stream.curators_list,
                            "students_list": learning_stream.students_list, "status": learning_stream.status})

        return learning_stream

    def get_learning_streams_list(self):
        """
        Возвращает список обучающих потоков

        Returns:
            learning_streams_list(List): список обучающих потоков
        """

        data_store = DataStore('learning_streams')

        learning_streams = data_store.get_rows()

        learning_streams_list = []

        for i_learning_stream in learning_streams:
            learning_streams_list.append(self.learning_stream_row_to_learning_stream(i_learning_stream))


        return learning_streams_list

    def get_learning_stream(self, _id):
        """
        Возвращает обучающий поток по id

        Args:
            _id(Int): идентификатор обучающего потока
        """

        data_store = DataStore('learning_streams')

        learning_stream = data_store.get_rows({"id": _id})

        if learning_stream != []:

            return self.learning_stream_row_to_learning_stream(learning_stream[0])
        else:
            return None

    def change_learning_stream(self, _learning_stream):
        """
        Изменяет данные обучающего потока

        Args:
            _learning_stream(Dict): обучающий поток
        """

        data_store = DataStore('learning_streams')

        learning_stream = self.learning_stream_row_to_learning_stream(_learning_stream)

        data_store.update_row({'id': learning_stream.id, "name": learning_stream.name,
                               'date_start': learning_stream.date_start.strftime('%d/%m/%Y'),
                               "date_end": learning_stream.date_end.strftime('%d/%m/%Y'), "teacher": learning_stream.teacher,
                               "id_course": learning_stream.course, "curators_list": learning_stream.curators_list,
                               "students_list": learning_stream.students_list, "status": learning_stream.status,
                               }, 'id')

        return learning_stream

