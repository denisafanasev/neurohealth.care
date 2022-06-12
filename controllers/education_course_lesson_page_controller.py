from services.course_service import CourseService
from services.room_chat_service import RoomChatService
from services.user_profile_service import UserProfileService
from services.user_manager_service import UserManagerService
from flask import Markup

class EducationCourseLessonPageController():

    def get_lesson(self, _id, _id_course, _id_video=1):
        """
        Возвращает данные урока

        Args:
            _id(Int): индентификатор урока
            _id_course(Int): индентификатор курса
            _id_video(Int): индентификатор видео
        """

        course_service = CourseService()

        module = course_service.get_lesson(_id, _id_course, _id_video)
        if module.lessons.task:
            module.lessons.task = Markup(module.lessons.task)

        if module.lessons.text:
            module.lessons.text = Markup(module.lessons.text)

        lesson = {
            "id_course": _id_course,
            "id_module": module.id,
            "name": module.name,
            "lesson": {
                "id": module.lessons.id,
                "id_module": module.lessons.id_module,
                "name": module.lessons.name,
                "link": module.lessons.link,
                "materials": module.lessons.materials,
                "text": module.lessons.text,
                # "task": module.lessons.task
            }
        }

        return lesson

    def room_chat_entry(self, _id_lesson="", _id_course="", _login_user="", _id_room_chat=None):
        """
        Подключает пользователя к чату

        Args:
            _id_lesson(Int): индентификатор урока
            _login_user(User): данные пользователя
            _id_course(Int): индентификатор курса
            _id_room_chat(Int): индентификатор чата

        Returns:
            chat(Dict): данные чата
        """

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
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _id_room_chat(Int): индентификатор чата
        """

        room_chat_service = RoomChatService()

        return room_chat_service.add_message(_message, _room_chat_id)

    def get_current_user(self):
        """
        Возвращает текущего пользователя

        Returns:
            Dict: пользователь
        """

        user_service = UserProfileService()

        user = user_service.get_current_user()

        return {"login": user.login, "role": user.role, "active_education_module": user.active_education_module,
                "education_module_expiration_date": str(user.education_module_expiration_date.strftime("%d/%m/%Y"))}

    def get_user_list(self):
        """
        Возвращает список пользователей

        Returns:
            List: список пользователей с типом User
        """

        user_service = UserManagerService()
        users = user_service.get_users()
        user_list = []

        for i_user in users:
            if i_user.role == "user":
                user_list.append(i_user.login)

        return user_list
    
    def get_course_by_id(self, _id):
        """
        Возвращает курс по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            course(Dict): данные курса
        """

        course_service = CourseService()
        course = course_service.get_course_by_id(_id)

        course_formated = {}
        course_formated["id"] = course.id
        course_formated["name"] = course.name
        course_formated["description"] = course.description
        course_formated["type"] = course.type

        return course_formated