from models.course_manager import CourseManager

class CourseService():

    def get_courses(self):

        course_manager = CourseManager()

        return course_manager.get_courses()

    def get_lesson(self, _id):

        course_manager = CourseManager()

        return course_manager.get_lesson(_id)