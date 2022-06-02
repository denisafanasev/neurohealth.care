from models.course_manager import CourseManager
from services.action_service import ActionService
from services.user_manager_service import UserManagerService

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