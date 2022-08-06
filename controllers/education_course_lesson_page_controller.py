from flask import Markup

from services.education_course_lesson_service import EducationCourseLessonService


class EducationCourseLessonPageController():

    def get_lesson(self, _user_id, _lesson_id, _id_course, _id_video=1, _id_room_chat=None):
        """
        Возвращает данные урока

        Args:
            _user_id(Int): индентификатор пользователя
            _lesson_id(Int): индентификатор урока
            _id_course(Int): индентификатор курса
            _id_video(Int): индентификатор видео
        """

        course_service = EducationCourseLessonService()

        if _id_room_chat is None:
            module = course_service.get_lesson(_user_id, _lesson_id, _id_course, _id_video, "no id_room_chat")
        else:
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
            },
            "available": course_service.is_course_module_avalable_for_user(_id_course, module.id, _user_id)
        }

        return lesson

    def room_chat_entry(self, _id_lesson="", _id_course="", _id_user="", _id_room_chat=None, _id_education_stream=None,
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

        education_course_service = EducationCourseLessonService()
        if _id_room_chat is None and _id_education_stream is None:
            _id_education_stream = "subscription"

        room_chat = education_course_service.room_chat_entry(_id_lesson, _id_course, _id_user, _id_room_chat,
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


    def add_message(self, _message, _room_chat_id, _user_id):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _id_room_chat(Int): индентификатор чата
        """

        education_course_service = EducationCourseLessonService()

        return education_course_service.add_message(_message, _room_chat_id, _user_id)

    def get_user_view_by_id_and_course_id(self, _user_id, _id_course):
        """
        Возвращает текущего пользователя

        Returns:
            Dict: пользователь
        """

        course_service = EducationCourseLessonService()

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
    
    def get_course_by_id(self, _id):
        """
        Возвращает курс по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            course(Dict): данные курса
        """

        course_service = EducationCourseLessonService()
        course = course_service.get_course_by_id(_id)

        course_formated = {}
        course_formated["id"] = course.id
        course_formated["name"] = course.name
        course_formated["description"] = course.description
        course_formated["type"] = course.type

        return course_formated

    def save_homework(self, _files_list, _id_room_chat, _user_id, _text, _id_lesson, _id_course):

        course_service = EducationCourseLessonService()

        course_service.save_homework(_files_list, _id_room_chat, _user_id, _text, _id_lesson, _id_course)

    def get_homework(self, _id_room_chat):
        """
        Возвращает данные домашней работы

        Args:
            _id_room_chat(Int): ID комнаты чата

        Return:
            Homework: домашняя работа
        """

        course_service = EducationCourseLessonService()

        homework = course_service.get_last_homework_by_id_room_chat(_id_room_chat)
        homework_view = None

        if homework is not None:
            if homework.homework_answer.answer:
                homework.homework_answer.answer = "Принято"
            else:
                homework.homework_answer.answer = "Не принято"

            homework_view = {
                "id": homework.id,
                "date_delivery": homework.date_delivery.strftime("%d/%m/%Y"),
                "users_files_list": [],
                "homework_answer": {
                    "id": homework.homework_answer.id,
                    "answer": homework.homework_answer.answer,
                    "status": homework.homework_answer.status
                },
                "text": Markup(homework.text)
            }

            for file in homework.users_files_list:
                if file.size // 1048576 == 0:
                    file_size = f"{round(file.size / 1024, 2)} кБ"
                else:
                    file_size = f"{round(file.size / 1048576, 2)} мБ"

                homework_view['users_files_list'].append({"name_file_unique": file.name_file_unique,
                                                          "size": file_size})

        return homework_view

    def get_neighboring_lessons(self, _user_id, _id_lesson, _id_course):
        """
        Возвращает данные соседних уроков текущего урока

        Args:
            _user_id(Int): ID текущего пользователя
            _id_lesson(Int): ID текущего урока
            _id_course(Int): ID текущего курса

        Returns:
            Dict: данные соседних уроков текущего урока
        """
        course_service = EducationCourseLessonService()

        neighboring_lessons = course_service.get_neighboring_lessons(_id_lesson, _id_course, _user_id)
        neighboring_lessons_view = {
            "next_lesson": None,
            "previous_lesson": None
        }
        if neighboring_lessons['next_lesson'] is not None:
            neighboring_lessons_view["next_lesson"] = {
                "id_course": _id_course,
                "id_module": neighboring_lessons['next_lesson'].id,
                "id": neighboring_lessons['next_lesson'].lessons.id
            }

        if neighboring_lessons['previous_lesson'] is not None:
            neighboring_lessons_view["previous_lesson"] = {
                "id_course": _id_course,
                "id_module": neighboring_lessons['previous_lesson'].id,
                "id": neighboring_lessons['previous_lesson'].lessons.id
            }

        return neighboring_lessons_view