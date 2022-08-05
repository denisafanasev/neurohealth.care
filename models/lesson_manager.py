from data_adapters.data_store import DataStore
from models.lesson import Lesson


class LessonManager():
    """
    Класс модели управления уроками курсов
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """
    def lesson_row_to_lesson(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о уроке в структуру Lesson

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Lesson: урок
        """

        lesson = Lesson(_id=_data_row.doc_id, _id_module=_data_row["id_module"], _name=_data_row["name"],
                        _materials=_data_row["materials"], _link=_data_row['link'])

        if _data_row.get("task") is not None:
            lesson.task = _data_row['task']

        if _data_row.get("text") is not None:
            lesson.text = _data_row['text']

        return lesson

    def get_lesson(self, _id, _id_video=1):
        """
        Возвращает данные урока

        Args:
            _id(Int): ID урока
            _id_video(Int): ID видео

        Return:
            Lesson: класс Lesson, обернутый в класс Module
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

    def get_neighboring_lessons(self, _id_lesson, _id_course):
        """
        Возвращает данные соседних уроков текущего урока

        Args:
            _id_lesson(Int): ID текущего урока
            _id_course(Int): ID текущего курса

        Returns:
            Dict: данные соседних уроков текущего урока
        """

        data_store_lessons = DataStore("lessons")

        current_lesson = data_store_lessons.get_row_by_id(_id_lesson)
        lessons_list = data_store_lessons.get_rows()

        index_current_lesson = lessons_list.index(current_lesson)
        neighboring_lessons = {
            "next_lesson": None,
            "previous_lesson": None
        }
        try:
            next_lesson = lessons_list[index_current_lesson + 1]
            neighboring_lessons['next_lesson'] = self.lesson_row_to_lesson(next_lesson)
        except IndexError:
            pass

        if index_current_lesson - 1 >= 0:
            previous_lesson = lessons_list[index_current_lesson - 1]
            neighboring_lessons['previous_lesson'] = self.lesson_row_to_lesson(previous_lesson)

        return neighboring_lessons