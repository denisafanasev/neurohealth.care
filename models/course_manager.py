from data_adapters.data_store import DataStore
from models.course import Course

class CourseManager():

    def course_row_to_course(self, _id, _name, _lessons):

        course = Course(_id, _name, _lessons)

        return course

    def get_courses(self):

        data_store_module = DataStore("modules")
        data_store_lessons = DataStore("lessons")

        modules = data_store_module.get_rows()

        modules_list = []

        for i_module in modules:

            lessons = data_store_lessons.get_rows({"id_module": i_module["id"]})
            lessons_list = []

            for i_lesson in lessons:
                lesson = {
                    "id": i_lesson["id"],
                    "name": i_lesson["name"]
                }

                lessons_list.append(lesson)

            modules_list.append(self.course_row_to_course(i_module["id"], i_module["name"], lessons_list))

        return modules_list

    def get_lesson(self, _id):

        data_store_lessons = DataStore("lessons")
        data_store_modules = DataStore("modules")

        lesson = data_store_lessons.get_rows({"id": _id})[0]
        module = data_store_modules.get_rows({"id": lesson["id_module"]})[0]

        return self.course_row_to_course(module["id"], module["name"], lesson)