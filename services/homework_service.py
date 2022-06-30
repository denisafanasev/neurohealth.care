from models.homework_manager import HomeworkManager
from services.upload_service import UploadService
from services.room_chat_service import RoomChatService
from services import course_service
from services import user_manager_service

class HomeworkService():

    def save_homework(self, _homework, _login_user, _id_room_chat):

        homework_manager = HomeworkManager()
        upload_service = UploadService()

        homework_files_list = upload_service.upload_files(_homework, _login_user)
        homework = homework_manager.create_homework(homework_files_list, _id_room_chat)

        homework_manager.create_homework_answer(homework.id)

    def get_homeworks_list(self):

        homework_manager = HomeworkManager()

        homework_list = homework_manager.get_homeworks()

        return homework_list

    def get_room_chat(self, _id_room_chat):

        room_chat_service = RoomChatService()

        return room_chat_service.get_room_chat(_id_room_chat=_id_room_chat)

    def get_course(self, _id_course):

        course_service_service = course_service.CourseService()

        return course_service_service.get_course_by_id(_id_course)

    def get_lesson(self, _id_lesson, _id_course):

        course_service_service = course_service.CourseService()

        return course_service_service.get_lesson(_id_lesson, _id_course, 1)

    # def get_learning_stream(self, _id_learning_stream):
    #
    #     stream_service = learning_stream_service.LearningStreamService()
    #
    #     return stream_service.get_learning_stream(_id_learning_stream)

    def get_current_user(self, _login_user):

        user_service = user_manager_service.UserManagerService()

        return user_service.get_current_user(_login_user)

    def change_homework_answer(self, _answer, _id_homework_answer):

        homework_manager = HomeworkManager()

        homework_manager.change_homework_answer(_answer, _id_homework_answer)

