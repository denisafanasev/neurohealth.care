from services.course_service import CourseService
from services.room_chat_service import RoomChatService
from services.user_profile_service import UserProfileService
from services.user_manager_service import UserManagerService
from flask import Markup

class EducationCourseLessonPageController():

    def get_lesson(self, _id, _id_course, _id_video=1):
        course_service = CourseService()

        course = course_service.get_lesson(_id, _id_course, _id_video)
        if course.lessons.task:
            course.lessons.task = Markup(course.lessons.task)

        if course.lessons.text:
            course.lessons.text = Markup(course.lessons.text)

        lesson = {
            "id_course": _id_course,
            "id": course.id,
            "name": course.name,
            "lesson": {
                "id": course.lessons.id,
                "id_module": course.lessons.id_module,
                "name": course.lessons.name,
                "link": course.lessons.link,
                "materials": course.lessons.materials,
                "text": course.lessons.text,
                "task": course.lessons.task
            }
        }

        return lesson

    def room_chat_entry(self, _id_lesson="", _id_course="", _login_user="", _id_room_chat=None):

        room_chat_service = RoomChatService()
        room_chat = room_chat_service.room_chat_entry(_id_lesson, _id_course, _login_user, _id_room_chat)

        chat = {
            "id": room_chat.id,
            "name": room_chat.name,
            "message": None
        }
        if room_chat.message is not None:

            message_list = []
            for i_message in room_chat.message:

                message = {
                    "id": i_message.id,
                    "text": Markup(i_message.text),
                    "name_sender": i_message.name_sender,
                    "files": None
                }
                if i_message.files is not None:

                    file_list = []
                    for i_file in i_message.files:

                        file = {
                            "name_file_user": i_file.name_file_user,
                            "name_file_unique": i_file.name_file_unique,
                            "path": i_file.path
                        }
                        file_list.append(file)

                    message["files"] = file_list

                message_list.append(message)

            chat["message"] = message_list

        return chat


    def add_message(self, _message, _room_chat_id):

        room_chat_service = RoomChatService()

        return room_chat_service.add_message(_message, _room_chat_id)

    def get_current_user(self):

        user_service = UserProfileService()

        user = user_service.get_current_user_role()

        return {"login": user.login, "role": user.role,
                "education_module_expiration_date": str(user.education_module_expiration_date.strftime("%d/%m/%Y"))}

    def get_user_list(self):

        user_service = UserManagerService()
        users = user_service.get_users()
        user_list = []

        for i_user in users:
            if i_user.role == "user":
                user_list.append(i_user.login)

        return user_list