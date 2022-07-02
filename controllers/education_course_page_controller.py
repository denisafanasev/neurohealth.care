from services.course_service import CourseService


class EducationCoursePageController():

    def get_course_modules_list(self, _id, _user_id):
        """
        Возвращает список модулей курса по id

        Args:
            _id(Int): индентификатор курса
            _user_id(Int): индентификатор пользователя

        Returns:
            modules_list_view(List): список модулей курса
        """

        course_service = CourseService()

        learning_stream = course_service.get_course_modules_list(_id, _login_user)
        # modules_list_view = {
        #     "id_learning_stream": learning_stream.id,
        #     "date_end": learning_stream.date_end,
        #     "modules_list": []
        # }
        modules_list_view = []
        for i_module in learning_stream:
            module = {}
            module["id"] = i_module.id
            module["name"] = i_module.name
            lesson_list = []

            for i_lesson in i_module.lessons:
                lesson = {
                    "id": i_lesson.id,
                    "name": i_lesson.name
                }
                lesson_list.append(lesson)

            module["lessons"] = lesson_list

            # проверим доступность модуля для пользователя
            module["available"] = course_service.is_course_module_avalable_for_user(_id, i_module.id, _user_id)

            modules_list.append(module)

        return modules_list

    def get_current_user(self, _id_course):
        """
        Возвращает данные текущего пользователя

        Returns:
            user(Dict): данные пользователя
        """

        # TODO: из контроллера можно вызывать только свой сервис, а не всего приложения
        course_service = CourseService()

        user = course_service.get_current_user(_id_course)
        user_view = {
            "login": user.login,
            "role": user.role,
            "active_education_module": user.active_education_module,
            "education_module_expiration_date": user.education_module_expiration_date.strftime("%d/%m/%Y"),
            "learning_stream": {}
        }

        if type(user.learning_stream_list) is not list:
            user_view['learning_stream'] = {
                "id": user.learning_stream_list.id,
                "date_end": user.learning_stream_list.date_end.strftime("%d/%m/%Y"),
                "status": user.learning_stream_list.status
            }

        return user_view
    
    def get_course_by_id(self, _id):
        """
        Возвращает курс по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            course(Dict): курс
        """

        course_service = CourseService()
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
