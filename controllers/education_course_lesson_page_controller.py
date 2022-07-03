from services.education_course_service import EducationCourseService
from services.room_chat_service import RoomChatService
from flask import Markup

class EducationCourseLessonPageController():

    def get_lesson(self, _user_id, _lesson_id, _id_course, _id_video=1):
        """
        Возвращает данные урока

        Args:
            _user_id(Int): индентификатор пользователя
            _lesson_id(Int): индентификатор урока
            _id_course(Int): индентификатор курса
            _id_video(Int): индентификатор видео
        """

        course_service = EducationCourseService()

        module = course_service.get_lesson(_user_id, _lesson_id, _id_course, _id_video)
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
                "task": module.lessons.task
            }
        }

        return lesson

    def room_chat_entry(self, _id_lesson="", _id_course="", _login_user="", _id_room_chat=None, _id_education_stream=None,
                        _id_module=None):
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
        if _id_room_chat is None and _id_education_stream is None:
            _id_education_stream = "subscription"

        room_chat = room_chat_service.room_chat_entry(_id_lesson, _id_course, _login_user, _id_room_chat,
                                                      _id_education_stream, _id_module)

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
                }

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

    def get_user_view_by_id_and_course_id(self, _user_id, _id_course):
        """
        Возвращает текущего пользователя

        Returns:
            Dict: пользователь
        """

        course_service = EducationCourseService()

        user = course_service.get_user_by_id(_user_id)

        user_view = {
            "login": user.login,
            "role": user.role,
            "active_education_module": user.active_education_module,
            "education_module_expiration_date": str(user.education_module_expiration_date.strftime("%d/%m/%Y")),
            "education_stream": {}
        }
        if type(user.education_stream_list) is not list:
            user_view["education_stream"] = {
                "id": user.education_stream_list.id,
                "date_end": user.education_stream_list.date_end,
                "status": user.education_stream_list.status
            }

        return user_view

    def get_user_list(self, _user_id):
        """
        Возвращает список пользователей

        Returns:
            List: список пользователей с типом User
        """

        course_service = EducationCourseService()
        users = course_service.get_user_list(_user_id)
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

        course_service = EducationCourseService()
        course = course_service.get_course_by_id(_id)

        course_formated = {}
        course_formated["id"] = course.id
        course_formated["name"] = course.name
        course_formated["description"] = course.description
        course_formated["type"] = course.type

        return course_formated

    def save_homework(self, _files_list, _id_room_chat):

        course_service = EducationCourseService()

        course_service.save_homework(_files_list, _id_room_chat)
