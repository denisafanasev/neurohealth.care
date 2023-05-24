from flask_babel import gettext

from data_adapters.data_store import DataStore
from models.lesson import Lesson


class EducationLessonManager():
    """
    Класс модели управления уроками курсов
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """
    def lesson_row_to_lesson(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация об уроке в структуру Lesson

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Lesson: урок
        """

        lesson = Lesson(_id=_data_row.doc_id, _id_module=_data_row["id_module"], _name=gettext(_data_row["name"]),
                        _materials=_data_row["materials"], _link=_data_row['link'])

        if _data_row.get("task") != "":
            lesson.task = gettext(_data_row['task'])

        if _data_row.get("text") != "":
            lesson.text = gettext(_data_row['text'])

        return lesson

    def get_lesson_by_id(self, _id, _id_video=1):
        """
        Возвращает данные урока по ID, а также данные видео по ID

        Args:
            _id(Integer): ID урока
            _id_video(Integer): ID видео. Defaults to 1

        Return:
            Lesson: урок
        """

        data_store_lessons = DataStore("lessons")

        lesson = data_store_lessons.get_row_by_id(_id)
        if lesson is not None:
            link_list = []
            if not lesson['link'] == "":
                for i_video in lesson['link']:
                    if i_video['id'] == _id_video:
                        link_list.append(i_video)
                    else:
                        link_list.append({"id": i_video['id']})
            else:
                link_list = None

            lesson["link"] = link_list

            return self.lesson_row_to_lesson(lesson)

    def get_neighboring_lessons(self, _id_lesson):
        """
        Возвращает данные соседних уроков текущего урока

        Args:
            _id_lesson(Int): ID текущего урока

        Returns:
            Dict: словарь с соседними уроками текущего урока
        """

        data_store_lessons = DataStore("lessons")

        current_lesson = data_store_lessons.get_row_by_id(_id_lesson)
        lessons_list = data_store_lessons.get_rows()
        # находим индекс, под которым храниться текущий урок
        index_current_lesson = lessons_list.index(current_lesson)
        neighboring_lessons = {
            "next_lesson": None,
            "previous_lesson": None
        }
        # находим соседние уроки
        try:
            next_lesson = lessons_list[index_current_lesson + 1]
            neighboring_lessons['next_lesson'] = self.lesson_row_to_lesson(next_lesson)
        except IndexError:
            pass

        if index_current_lesson - 1 >= 0:
            previous_lesson = lessons_list[index_current_lesson - 1]
            neighboring_lessons['previous_lesson'] = self.lesson_row_to_lesson(previous_lesson)

        return neighboring_lessons

    def get_lessons_list_by_id_module(self, _id_module):
        """
        Возвращает список уроков, принадлежащих одному модулю

        Args:
            _id_module(Int): ID модуля

        Return:
            List: список уроков
        """
        data_store = DataStore("lessons")

        lessons_data_list = data_store.get_rows({"id_module": _id_module})
        lessons_list = []
        for lesson_data in lessons_data_list:
            lessons_list.append(self.lesson_row_to_lesson(lesson_data))

        return lessons_list

    def get_lessons(self):
        """
        Возвращает все уроки, которые есть в базе данных

        Return:
            lesson_list(List): список уроков
        """
        data_store = DataStore('lessons')

        lessons_data_list = data_store.get_rows()
        lessons_list = [self.lesson_row_to_lesson(lesson) for lesson in lessons_data_list if lesson['task'] != '']

        return lessons_list
