from models.course_manager import CourseManager

class CourseService():

    def get_course(self, _id):

        course_manager = CourseManager()

        return course_manager.get_course(_id)

    def get_lesson(self, _id, _id_course):

        course_manager = CourseManager()

        return course_manager.get_lesson(_id, _id_course)

    def get_courses(self):

        course_manager = CourseManager()

        return course_manager.get_courses()