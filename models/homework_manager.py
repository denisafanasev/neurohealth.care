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

        return homework

    def homework_answer_row_to_homework_answer(self, _data_row):

        homework_answer = HomeworkAnswer(_id=_data_row['id'], _id_homework=_data_row['id_homework'],
                                         _answer=_data_row['answer'])

        if _data_row.get("answer") is not None:
            homework_answer.answer = _data_row['answer']
        else:
            homework_answer.answer = False

        return homework_answer

    def save_homework(self, _homework_files_list, _id_room_chat):
        """
        Сохраняет данные файла

        Args:
            _homeworks(Dict): данные сданной домашней работы
            _id_room_chat(Int): индетификатор чата
        """

        data_store = DataStore("homeworks")

        row_count = data_store.get_rows_count()

        homework = self.homework_row_to_homework({"id": row_count + 1, "id_room_chat": _id_room_chat,
                                                  "users_files_list": _homework_files_list})

        data_store.add_row({"id": homework.id, "id_room_chat": homework.id_room_chat,
                            "users_files_list": homework.users_files_list})

        return homework

    # def get_homeworks(self, _name_file_list):
    #     """
    #     Возвращает данные файлов из чата
    #
    #     Args:
    #         _name_file_list(List): список уникальных имен файлов домашнего задания
    #     """
    #
    #     data_store = DataStore("homeworks")
    #     homework_list = []
    #
    #     for i_file in _name_file_list:
    #         file = data_store.get_rows({"name_file_unique": i_file})[0]
    #         homework = self.homework_row_to_homework(file)
    #         homework_list.append(homework.name_file_unique)
    #
    #     return homework_list

    def create_homework_answers(self, _id_homework):

        data_store = DataStore("homework_answers")

        row_count = data_store.get_rows_count()
        answer = {
            "id": row_count + 1,
            "answer": False,
            "id_homework": _id_homework
        }

        homework_answer = self.homework_answer_row_to_homework_answer(answer)

        data_store.add_row({"id": homework_answer.id, "answer": homework_answer.answer,
                            "id_homework": homework_answer.id_homework})

