from services.course_service import CourseService


class EducationCoursePageController():

    def get_course_modules_list(self, _id):
        """
        Возвращает список модулей курса по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            modules_list(List): список модулей курса
        """

        course_service = CourseService()

        course = course_service.get_course_modules_list(_id)
        modules_list = []

        for i_module in course:
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

            modules_list.append(module)

        return modules_list

    def get_current_user(self, _id_course):
        """
        Возвращает данные текущего пользователя

        Returns:
            user(Dict): данные пользователя
        """

        # TODO: из контроллера можно вызывать только свой сервис, а
        course_service = CourseService()

        user = course_service.get_current_user()
        user_view = {
            "login": user.login,
            "role": user.role,
            "active_education_module": user.active_education_module,
            "education_module_expiration_date": user.education_module_expiration_date.strftime("%d/%m/%Y"),
            "learning_stream": {}
        }

        # if type(user.learning_stream_list) is not list:
        #     user_view['learning_stream'] = {
        #         "id": user.learning_stream_list.id,
        #         "date_end": user.learning_stream_list.date_end.strftime("%d/%m/%Y"),
        #         "status": user.learning_stream_list.status
        #     }

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