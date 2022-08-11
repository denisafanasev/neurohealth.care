from datetime import datetime, timedelta

from models.homework import Homework
from data_adapters.data_store import DataStore


class HomeworkManager():

    def homework_row_to_homework(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о файле в структуру Homework
        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер
        Returns:
            Homework: домашняя работа
        """

        homework = Homework(_id=_data_row.doc_id, _users_files_list=_data_row['users_files_list'],
                            _text=_data_row['text'], _id_lesson=_data_row['id_lesson'], _id_user=_data_row['id_user'],
                            _status=_data_row['status'])

        if _data_row.get("date_delivery") is not None:
            homework.date_delivery = datetime.strptime(_data_row['date_delivery'], "%d/%m/%Y")
        else:
            homework.date_delivery = datetime.today()

        return homework

    def create_homework(self, _homework_files_list, _id_room_chat, _text, _id_user, _id_course, _id_lesson):
        """
        Сохраняет домашнюю работу
        Args:
            _homework_files_list(Dict): данные сданной домашней работы
            _id_room_chat(Int): ID чата
            _text(String): ответ на задание
            _id_user(Int): ID пользователя
            _id_course(Int): ID курса
            _id_lesson(Int): ID урока

        Return:
            Homework: домашняя работа
        """

        data_store = DataStore("homeworks")


        homework = Homework(_users_files_list= _homework_files_list, _text=_text, _id_user=_id_user,
                            _id_lesson=_id_lesson, _status=None)

        data_store.add_row({"users_files_list": homework.users_files_list,
                            "date_delivery": homework.date_delivery.strftime("%d/%m/%Y"), "text": homework.text,
                            "id_user": homework.id_user, "id_lesson": homework.id_lesson, "status": homework.status})

        return homework

    def get_homeworks(self):
        """
        Возвращает список домашних работ пользователей
        Returns:
            List: список домашних работ
        """

        data_store = DataStore("homeworks")

        homeworks = data_store.get_rows()
        homework_list = []
        for homework in homeworks:
            if homework.get("text") is None:
                data_store.update_row({"id": homework["id"], "text": ""}, "id")
                homework['text'] = ""

            homework_list.append(self.homework_row_to_homework(homework))

        return homework_list

    def get_homeworks_list_by_id_lesson(self, _id_lesson, _id_user):
        """
        Возвращает список домашних работ по ID урока и ID пользователя

        Args:
            _id_lesson(Int): ID
            _id_user(Int): ID

        Return:
            List: список домашних работ
        """

        data_store = DataStore("homeworks")

        homeworks_list = data_store.get_rows({"id_lesson": _id_lesson, "id_user": _id_user})
        homeworks = []

        for homework in homeworks_list:
            if homework.get("text") is None:
                data_store.update_row({"id": homework["id"], "text": ""}, "id")
                homework['text'] = ""

            homeworks.append(self.homework_row_to_homework(homework))

        return homeworks

    def get_homework_by_id(self, _id):
        """
        Возвращает домашнюю работу по ID

        Args:
            _id(Int): ID домашней работы

        Return:
            Homework: домашняя работа
        """

        data_store = DataStore("homeworks")

        homework = data_store.get_row_by_id(_id)

        return self.homework_row_to_homework(homework)

    def homework_answer_accepted(self, _id_homework):
        """
        Меняет статус проверки домашней работы на "Принято"

        Args:
            _id_homework(Int): ID домашней работы

        Returns:
            Boolean: новый статус домашней работы
        """

        data_store = DataStore("homeworks")

        homework_data = data_store.get_row_by_id(_id_homework)
        homework = self.homework_row_to_homework(homework_data)
        homework.status = True

        data_store.update_row_by_doc_id({"status": homework.status}, homework.id)

        return homework

    def homework_answer_no_accepted(self, _id_homework):
        """
        Меняет статус проверки домашней работы на "Не принято"

        Args:
            _id_homework(Int): ID домашней работы

        Returns:
            Boolean: новый статус домашней работы
        """

        data_store = DataStore("homeworks")

        homework_data = data_store.get_row_by_id(_id_homework)
        homework = self.homework_row_to_homework(homework_data)
        homework.status = False

        data_store.update_row_by_doc_id({"status": homework.status}, homework.id)

        return homework