from distutils.command.config import config
from data_adapters.data_store import DataStore
from models.course import Module, Lesson, CoursesList
import os
import config

class CourseManager():

    def lesson_row_to_lesson(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о уроке в структуру Lesson

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Lesson: урок
        """

        lesson = Lesson(_data_row["id"], _data_row["id_module"], _data_row["name"], _data_row["materials"],
                        _data_row["link"], _data_row["text"], _data_row["task"])

        return lesson

    def courses_list_row_to_courses_list(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о уроке в структуру CoursesList

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            CoursesList: список курсов
        """

        courses_list = CoursesList(_data_row["id"], _data_row["name"], _data_row["description"], _data_row["image"])

        return courses_list

    def course_row_to_course(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о уроке в структуру Course

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Module: курс
        """

        course = Module(_data_row["id"], _data_row["name"], _data_row["lessons"])

        return course

    def get_course(self, _id=1):

        try:
            data_store_module = DataStore(f"course_{_id}/modules")
            data_store_lessons = DataStore(f"course_{_id}/lessons")
        except FileNotFoundError:
            # os.mkdir(f"data/course_{_id}")
            os.mkdir(config.DATA_FOLDER+"course_{"+str(_id)+"}")
            data_store_module = DataStore(f"course_{_id}/modules")
            data_store_lessons = DataStore(f"course_{_id}/lessons")

        modules = data_store_module.get_rows()

        modules_list = []

        for i_module in modules:

            lessons = data_store_lessons.get_rows({"id_module": i_module["id"]})
            lessons_list = []

            for i_lesson in lessons:

                if not i_lesson.get("task"):
                    i_lesson["task"] = None

                if not i_lesson.get("text"):
                    i_lesson["text"] = None

                lesson = self.lesson_row_to_lesson(i_lesson)


                lessons_list.append(lesson)

            i_module["lessons"] = lessons_list

            modules_list.append(self.course_row_to_course(i_module))

        return modules_list

    def get_lesson(self, _id, _id_course=1, _id_video=1):

        data_store_lessons = DataStore(f"course_{_id_course}/lessons")
        data_store_modules = DataStore(f"course_{_id_course}/modules")

        lesson = data_store_lessons.get_rows({"id": _id})[0]
        if not lesson.get("task"):
            lesson["task"] = None

        if not lesson.get("text"):
            lesson["text"] = None

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

        return self.course_row_to_course(module)

    def get_courses(self):

        data_store = DataStore("courses_list")

        courses_list = data_store.get_rows()
        courses = []

        for i_course in courses_list:
            try:
                data_store_course = DataStore(f"course_{i_course['id']}/settings")
            except FileNotFoundError:
                # os.mkdir(f"data/course_{i_course['id']}")
                os.mkdir(config.DATA_FOLDER+"course_{"+str(i_course['id'])+"}")
                data_store_course = DataStore(f"course_{i_course['id']}/settings")

            try:
                i_course['image'] = data_store_course.get_rows()[0]["image"]
            except IndexError:
                i_course['image'] = ""

            courses.append(self.courses_list_row_to_courses_list(i_course))

        return courses