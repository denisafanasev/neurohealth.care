from datetime import datetime, timedelta

from models.homework import Homework, HomeworkAnswer
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

        homework = Homework(_id=_data_row['id'], _id_room_chat=_data_row['id_room_chat'],
                            _users_files_list=_data_row['users_files_list'])

        if _data_row.get("date_delivery") is not None:
            homework.date_delivery = datetime.strptime(_data_row['date_delivery'], "%d/%m/%Y")
        else:
            homework.date_delivery = datetime.today()

        if _data_row.get("homework_answer") is not None:
            homework.homework_answer = _data_row['homework_answer']

        return homework

    def homework_answer_row_to_homework_answer(self, _data_row):

        homework_answer = HomeworkAnswer(_id=_data_row['id'], _id_homework=_data_row['id_homework'],
                                         _answer=_data_row['answer'])

        if _data_row.get("answer") is not None:
            homework_answer.answer = _data_row['answer']
        else:
            homework_answer.answer = None

        if homework_answer.answer is not None:
            homework_answer.status = "проверено"
        else:
            homework_answer.status = "не проверено"

        return homework_answer

    def create_homework(self, _homework_files_list, _id_room_chat):
        """
        Сохраняет данные файла

        Args:
            _homework_files_list(Dict): данные сданной домашней работы
            _id_room_chat(Int): индетификатор чата
        """

        data_store = DataStore("homeworks")

        row_count = data_store.get_rows_count()

        homework = self.homework_row_to_homework({"id": row_count + 1, "id_room_chat": _id_room_chat,
                                                  "users_files_list": _homework_files_list})

        data_store.add_row({"id": homework.id, "id_room_chat": homework.id_room_chat,
                            "users_files_list": homework.users_files_list, "date_delivery": homework.date_delivery.strftime("%d/%m/%Y")})

        return homework

    def get_homeworks(self):
        """

        """

        data_store = DataStore("homeworks")

        homeworks = data_store.get_rows()
        homework_list = []
        for homework in homeworks:
            homework['homework_answer'] = self.get_homework_answer(homework['id'])
            homework_list.append(self.homework_row_to_homework(homework))

        return homework_list

    def create_homework_answer(self, _id_homework):

        data_store = DataStore("homework_answers")

        row_count = data_store.get_rows_count()
        answer = {
            "id": row_count + 1,
            "answer": None,
            "id_homework": _id_homework
        }

        homework_answer = self.homework_answer_row_to_homework_answer(answer)

        data_store.add_row({"id": homework_answer.id, "answer": homework_answer.answer,
                            "id_homework": homework_answer.id_homework})

    def get_homework_answer(self, _id_homework):

        data_store = DataStore("homework_answers")

        homework_answer = data_store.get_rows({"id_homework": int(_id_homework)})[0]

        return self.homework_answer_row_to_homework_answer(homework_answer)

    def change_homework_answer(self, _answer, _id_homework_answer):

        data_store = DataStore("homework_answers")

        answer = data_store.get_rows({"id": _id_homework_answer})[0]

        homework_answer = self.homework_answer_row_to_homework_answer(answer)

        if _answer == "True":
            homework_answer.answer = True
        elif _answer == "False":
            homework_answer.answer = False

        data_store.update_row({"id": homework_answer.id, "answer": homework_answer.answer}, "id")
