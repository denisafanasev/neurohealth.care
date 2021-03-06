from distutils.command.config import config
from data_adapters.data_store import DataStore
from models.course import Module, Lesson, CoursesList, Course
import os
import config

class EducationCourseManager():

    def lesson_row_to_lesson(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о уроке в структуру Lesson

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Lesson: урок
        """

        lesson = Lesson(_id=_data_row["id"], _id_module=_data_row["id_module"], _name=_data_row["name"],
                        _materials=_data_row["materials"], _link=_data_row['link'])

        if _data_row.get("task") is not None:
            lesson.task = _data_row['task']

        if _data_row.get("text") is not None:
            lesson.text = _data_row['text']

        return lesson

    def courses_list_row_to_courses_list(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о уроке в структуру CoursesList

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            CoursesList: список курсов
        """

        courses_list = CoursesList(_data_row["id"], _data_row["name"], _data_row["description"], _data_row["image"], _data_row["type"])

        return courses_list

    def module_row_to_module(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о уроке в структуру Course

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Module: курс
        """

        module = Module(_data_row["id"], _data_row["name"], _data_row["lessons"])

        return module
    
    def course_row_to_course(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о уроке в структуру Lesson

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Lesson: урок
        """

        course = Course(_data_row["id"], _data_row["name"], _data_row["description"], _data_row["type"])

        return course

    def get_course_modules_list(self, _id=1):
        """
        Возвращает список модулей курса по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            modules_list(List): списко модулей курса
        """

        try:
            data_store_module = DataStore(f"course_{_id}/modules")
            data_store_lessons = DataStore(f"course_{_id}/lessons")
        except FileNotFoundError:
            # os.mkdir(f"data/course_{_id}")
            os.mkdir(config.DATA_FOLDER+"course_"+str(_id))
            data_store_module = DataStore(f"course_{_id}/modules")
            data_store_lessons = DataStore(f"course_{_id}/lessons")

        modules = data_store_module.get_rows()

        modules_list = []

        for i_module in modules:

            lessons = data_store_lessons.get_rows({"id_module": i_module["id"]})
            lessons_list = []

            for i_lesson in lessons:
                lesson = self.lesson_row_to_lesson(i_lesson)
                lessons_list.append(lesson)

            i_module["lessons"] = lessons_list

            modules_list.append(self.module_row_to_module(i_module))

        return modules_list

    def get_lesson(self, _id, _id_course=1, _id_video=1):
        """
        Возвращает данные урока

        Args:
            _id(Int): индентификатор урока
            _id_course(Int): индентификатор курса
            _id_video(Int): индентификатор видео

        Return:
            Lesson: класс Lesson, обернутый в класс Module
        """

        data_store_lessons = DataStore(f"course_{_id_course}/lessons")
        data_store_modules = DataStore(f"course_{_id_course}/modules")

        lesson = data_store_lessons.get_rows({"id": _id})
        if lesson != []:
            lesson = lesson[0]

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

            module = data_store_modules.get_rows({"id": lesson["id_module"]})[0]
            module["lessons"] = self.lesson_row_to_lesson(lesson)

            return self.module_row_to_module(module)

    def get_courses(self):
        """
        Возвращает список курсов

        Returns:
            courses(List): список курсов
        """

        data_store = DataStore("courses_list")

        courses_list = data_store.get_rows()
        courses = []

        for i_course in courses_list:
            try:
                data_store_course = DataStore(f"course_{i_course['id']}/settings")
            except FileNotFoundError:
                # os.mkdir(f"data/course_{i_course['id']}")
                os.mkdir(config.DATA_FOLDER+"course_"+str(i_course['id']))
                data_store_course = DataStore(f"course_{i_course['id']}/settings")

            try:
                i_course['image'] = data_store_course.get_rows()[0]["image"]
            except IndexError:
                i_course['image'] = ""

            courses.append(self.courses_list_row_to_courses_list(i_course))

        return courses
    
    def get_course_by_id(self, _id):
        """
        Возвращает курс по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            course(Course): курс
        """

        course = None

        data_store = DataStore("courses_list")
        course_data = data_store.get_row_by_id(_id)

        if course_data is not None:

            course = self.course_row_to_course(course_data)

        return course

    def get_neighboring_lessons(self, _id_lesson, _id_course):
        """
        Возвращает данные соседних уроков текущего урока

        Args:
            _id_lesson(Int): ID текущего урока
            _id_course(Int): ID текущего курса

        Returns:
            Dict: данные соседних уроков текущего урока
        """

        data_store_lessons = DataStore(f"course_{_id_course}/lessons")
        data_store_modules = DataStore(f"course_{_id_course}/modules")

        current_lesson = data_store_lessons.get_rows({"id": _id_lesson})[0]
        lessons_list = data_store_lessons.get_rows()

        index_current_lesson = lessons_list.index(current_lesson)
        neighboring_lessons = {}
        try:
            next_lesson = lessons_list[index_current_lesson + 1]
            module_next_lesson = data_store_modules.get_rows({"id": next_lesson["id_module"]})[0]
            module_next_lesson["lessons"] = self.lesson_row_to_lesson(next_lesson)
            neighboring_lessons['next_lesson'] = self.module_row_to_module(module_next_lesson)
        except IndexError:
            neighboring_lessons['next_lesson'] = None

        if index_current_lesson - 1 >= 0:
            previous_lesson = lessons_list[index_current_lesson - 1]
            module_previous_lesson = data_store_modules.get_rows({"id": previous_lesson["id_module"]})[0]
            module_previous_lesson["lessons"] = self.lesson_row_to_lesson(previous_lesson)
            neighboring_lessons['previous_lesson'] = self.module_row_to_module(module_previous_lesson)
        else:
            neighboring_lessons['previous_lesson'] = None

        return neighboring_lessons
