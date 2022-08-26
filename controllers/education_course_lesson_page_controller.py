from flask import Markup

from services.education_course_lesson_service import EducationCourseLessonService


class EducationCourseLessonPageController():

    def get_lesson(self, _user_id, _lesson_id, _id_video=1):
        """
        Возвращает данные урока

        Args:
            _user_id(Int): ID пользователя
            _lesson_id(Int): ID урока
            _id_video(Int): ID видео

        Returns:
            Dict: данные урока
        """

        course_service = EducationCourseLessonService()

        module = course_service.get_lesson(_user_id, _lesson_id, _id_video)
        if module is not None:
            if module.lessons.task:
                module.lessons.task = Markup(module.lessons.task)

            if module.lessons.text:
                module.lessons.text = Markup(module.lessons.text)

            lesson = {
                "id_course": module.id_course,
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
                "available": course_service.is_course_module_avalable_for_user(module.id_course, module.id, _user_id)
            }

            return lesson

    def room_chat_entry(self, _id_room_chat=None, _id_user=None):
        """
        Подключает пользователя к чату

        Args:
            _id_room_chat(Int): ID чата
            _id_user(Int): ID пользователя

        Returns:
            Dict: данные чата
        """

        education_course_service = EducationCourseLessonService()

        room_chat = education_course_service.room_chat_entry(_id_room_chat, _id_user)
        if room_chat is not None:
            chat = {
                "id": room_chat.id,
                "message": None
            }
            if room_chat.message is not None:
                message_list = []
                for i_message in room_chat.message:
                    # ищем данные пользователя, который отправил данное сообщения
                    user = education_course_service.get_user_by_id(i_message.id_user)
                    message = {
                        "id": i_message.id,
                        "text": Markup(i_message.text),
                        "id_user": i_message.id_user,
                        "name": user.name
                    }

                    message_list.append(message)

                chat["message"] = message_list

            return chat

    def add_message(self, _message, _id_lesson):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _id_lesson(Int): ID урока
        """

        education_course_service = EducationCourseLessonService()

        education_course_service.add_message(_message, _id_lesson)

    def get_user_view_by_id_and_course_id(self, _user_id):
        """
        Возвращает текущего пользователя

        Args:
            _user_id(Int): ID текущего пользователя

        Returns:
            Dict: пользователь
        """

        course_service = EducationCourseLessonService()

        user = course_service.get_user_by_id(_user_id)

        user_view = {
            "user_id": user.user_id,
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
            _id(Int): ID курса

        Returns:
            Dict: данные курса
        """

        course_service = EducationCourseLessonService()
        course = course_service.get_course_by_id(_id)

        course_formated = {}
        course_formated["id"] = course.id
        course_formated["name"] = course.name
        course_formated["description"] = course.description
        course_formated["type"] = course.type

        return course_formated

    def save_homework(self, _files_list, _user_id, _text, _id_lesson):
        """
        Сохраняет домашнюю работы

        Args:
            _files_list(List): список файлов, сданных вместе с домашней работой
            _user_id(Int): ID пользователя
            _text(String): текст домашней работы
            _id_lesson(Int): ID урока
        """
        course_service = EducationCourseLessonService()

        course_service.save_homework(_files_list, _user_id, _text, _id_lesson)

    def get_last_homework(self, _id_lesson, _user_id):
        """
        Возвращает данные последней сданной домашней работы по уроку

        Args:
            _id_lesson(Int): ID урока
            _user_id(Int): ID текущего пользователя

        Return:
            Homework: домашняя работа
        """

        course_service = EducationCourseLessonService()

        homework = course_service.get_last_homework(_id_lesson, _user_id)
        homework_view = None
        if homework is not None:
            if homework.status is None:
                homework.status = "не проверенно"
            elif homework.status:
                homework.status = "Принято"
            else:
                homework.status = "Не принято"

            homework_view = {
                "id": homework.id,
                "date_delivery": homework.date_delivery.strftime("%d/%m/%Y"),
                "users_files_list": [],
                "status": homework.status,
                "text": Markup(homework.text)
            }
            # переводим размер файлов, сданной вместе с домашней работой, из бит в кб или мб
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
            room_chat = course_service.get_room_chat(neighboring_lessons['next_lesson'].lessons.id, _user_id)
            neighboring_lessons_view["next_lesson"] = {
                "id_course": _id_course,
                "id_module": neighboring_lessons['next_lesson'].id,
                "id": neighboring_lessons['next_lesson'].lessons.id,
                "id_room_chat": None
            }
            if room_chat is not None:
                neighboring_lessons_view['next_lesson']['id_room_chat'] = room_chat.id

        if neighboring_lessons['previous_lesson'] is not None:
            room_chat = course_service.get_room_chat(neighboring_lessons['previous_lesson'].lessons.id, _user_id)
            neighboring_lessons_view["previous_lesson"] = {
                "id_course": _id_course,
                "id_module": neighboring_lessons['previous_lesson'].id,
                "id": neighboring_lessons['previous_lesson'].lessons.id,
                "id_room_chat": None
            }
            if room_chat is not None:
                neighboring_lessons_view['previous_lesson']['id_room_chat'] = room_chat.id

        return neighboring_lessons_view

    def get_room_chat(self, _id_lesson, _id_user):
        """
        Возвращает данные комнаты чата по ID урока и пользователя

        Args:
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID текущего пользователя

        Returns:
            Dict: данные комнаты чата
        """
        course_service = EducationCourseLessonService()

        room_chat = course_service.get_room_chat(_id_lesson, _id_user)
        if room_chat is not None:
            room_chat_view = {
                "id": room_chat.id,
                "id_lesson": room_chat.id_lesson,
                "id_user": room_chat.id_user,
                "message": []
            }
            if room_chat.message is not None:
                for message in room_chat.message:
                    user = course_service.get_user_by_id(message.id_user)
                    room_chat_view['message'].append({
                        "id": message.id,
                        "id_room_chat": message.id_room_chat,
                        "id_user": message.id_user,
                        "name": user.name,
                        "text": Markup(message.text),
                        "date_send": message.date_send
                    })

            return room_chat_view