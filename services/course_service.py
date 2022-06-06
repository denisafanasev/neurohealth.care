from models.course_manager import CourseManager
from services.action_service import ActionService
from models.user_manager import UserManager

class CourseService():

    def get_course(self, _id):

        course_manager = CourseManager()

        return course_manager.get_course(_id)

    def get_lesson(self, _id, _id_course, _id_video):

        course_manager = CourseManager()
        action_service = ActionService()

        lesson = course_manager.get_lesson(_id, _id_course, _id_video)

        action_service.add_notifications(lesson, "view", "course_manager")

        return lesson

    def get_courses(self):

        course_manager = CourseManager()

        return course_manager.get_courses()

    def get_current_user(self):

        user_manager = UserManager()

        return user_manager.get_user_by_id(user_manager.get_current_user_id())

    def get_course_by_id(self, _id):

        course_manager = CourseManager()

        return course_manager.get_course_by_id(_id)