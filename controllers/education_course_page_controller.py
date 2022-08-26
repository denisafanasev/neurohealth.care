from services.education_course_service import EducationCourseService


class EducationCoursePageController():
    """
    Сервис для страницы курса
    """    

    def get_course_modules_list(self, _id, _user_id):
        """
        Возвращает список модулей курса по id

        Args:
            _id(Int): ID курса
            _user_id(Int): ID пользователя

        Returns:
            List: список модулей курса
        """

        course_service = EducationCourseService()

        education_stream = course_service.get_course_modules_list(_id)

        modules_list = []
        module_order = 0
        if education_stream is not None:
            for i_module in education_stream:

                module_order += 1

                module = {}
                module["id"] = i_module.id
                module["name"] = i_module.name
                module["order"] = module_order
                lesson_list = []

                # проверим доступность модуля для пользователя
                module["available"] = course_service.is_course_module_avalable_for_user(_id, i_module.id, _user_id)
                user_role = course_service.get_user_by_id(_user_id).role

                for i_lesson in i_module.lessons:
                    lesson = {
                        "id": i_lesson.id,
                        "name": i_lesson.name,
                        "homework": None,
                        "task": i_lesson.task,
                        "id_room_chat": None
                    }

                    if user_role != "superuser":
                        if ((module['available'] and i_module.id <= 8) or i_module.id == 1) and i_lesson.task is not None:
                            last_homeworks = course_service.get_last_homework(i_lesson.id, _user_id)
                            if last_homeworks is not None:
                                if last_homeworks.status is None:
                                    last_homeworks.status = "Не проверено"
                                elif last_homeworks.status:
                                    last_homeworks.status = "Принято"
                                else:
                                    last_homeworks.status = "Не принято"

                                lesson['homework'] = {
                                    "date_delivery": last_homeworks.date_delivery.strftime("%d/%m/%Y"),
                                    "status": last_homeworks.status,
                                }
                            room_chat = course_service.get_room_chat(i_lesson.id, _user_id)
                            if room_chat is not None:
                                lesson['id_room_chat'] = room_chat.id
                                lesson['unread_message_amount'] = room_chat.unread_message_amount

                    lesson_list.append(lesson)

                module["lessons"] = lesson_list

                modules_list.append(module)

            return modules_list

    def get_user_view_for_course_by_id(self, _user_id, _id_course):
        """
        Возвращает представление текущего пользователя

        Returns:
            Dict: данные пользователя
        """

        course_service = EducationCourseService()
        user = course_service.get_user_by_id_and_course_id(_user_id, _id_course)

        user_view = {
            "login": user.login,
            "role": user.role,
            "active_education_module": user.active_education_module,
            "education_module_expiration_date": user.education_module_expiration_date.strftime("%d/%m/%Y"),
            "education_stream": {}
        }
        if type(user.education_stream_list) is not list:
            user_view['education_stream'] = {
                "id": user.education_stream_list.id,
                "date_end": user.education_stream_list.date_end.strftime("%d/%m/%Y"),
                "status": user.education_stream_list.status
            }

        return user_view
    
    def get_course_by_id(self, _id):
        """
        Возвращает курс по id

        Args:
            _id(Int): ID курса

        Returns:
            course(Dict): курс
        """

        course_service = EducationCourseService()
        course = course_service.get_course_by_id(_id)

        course_formated = {}
        if course is not None:
            course_formated["id"] = course.id
            course_formated["name"] = course.name
            course_formated["description"] = course.description
            course_formated["type"] = course.type
        else:
            course_formated["id"] = _id
            course_formated['name'] = None
            course_formated['type'] = None

        return course_formated

    def add_action(self, _id_lesson, _id_user):
        """
        Создает событие "Просмотр урока пользователем"

        Args:
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID текущего пользователя
        """
        course_service = EducationCourseService()

        course_service.add_action(_id_lesson, _id_user)
