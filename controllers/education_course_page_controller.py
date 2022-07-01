from services.course_service import CourseService


class EducationCoursePageController():

    def get_course_modules_list(self, _id, _user_id):
        """
        Возвращает список модулей курса по id

        Args:
            _id(Int): индентификатор курса
            _user_id(Int): индентификатор пользователя

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

            # проверим доступность модуля для пользователя
            module["available"] = course_service.is_course_module_avalable_for_user(_id, i_module.id, _user_id)

            modules_list.append(module)

        return modules_list

    def get_current_user(self):
        """
        Возвращает данные текущего пользователя

        Returns:
            user(Dict): данные пользователя
        """

        # TODO: из контроллера можно вызывать только свой сервис, а не всего приложения
        course_service = CourseService()

        user = course_service.get_current_user()

        return {"id": user.user_id, "login": user.login, "role": user.role, "active_education_module": user.active_education_module,
                "education_module_expiration_date": str(user.education_module_expiration_date.strftime("%d/%m/%Y"))}
    
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