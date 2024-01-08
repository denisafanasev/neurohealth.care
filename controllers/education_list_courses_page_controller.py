from services.education_list_courses_service import EducationListCoursesService


class EducationListCoursesPageController():
    """
    EducationListCoursesPageController - класс контроллера представления списка курсов.
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответсвующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    def get_courses(self):
        """
        Возвращает список курсов

        Returns:
            courses(List): список курсов
        """

        course_service = EducationListCoursesService()

        courses = course_service.get_courses()
        courses_list = []

        for i_course in courses:
            course = {
                "id": i_course.id,
                "name": i_course.name,
                "description": i_course.description,
                "image": i_course.image,
                "type": i_course.type
            }

            courses_list.append(course)

        return courses_list
    
    def get_user_view_by_id(self, _user_id):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)

        Returns:
            User: пользователь
        """
        course_service = EducationListCoursesService()

        user = course_service.get_user_by_id(_user_id)

        return {"login": user.login, "role": user.role, "active_education_module": user.active_education_module,
                "education_module_expiration_date": str(user.education_module_expiration_date.strftime("%d/%m/%Y"))}

    def get_user_education_progress(self, _user_id):
        """
        Возвращает количество выполненных/не выполненных модулей/домашних заданий

        Args:
            _user_id(Int): ID пользователя

        Returns:
            data_list_view(Dict):
                -education_stream_name (Str): название потока, в котором есть пользователь
                -amount_modules_passed (Int): количество невыполненных модулей
                -amount_modules_no_passed (Int): количество не выполненных модулей
                -amount_homework_accepted (Int): количество выполненных домашних заданий
                -amount_homework_no_accepted (Int): количество невыполненных домашних заданий

        """
        course_service = EducationListCoursesService()

        education_streams_list = course_service.get_education_streams(_user_id)
        data_list_view = []
        if education_streams_list is not None:
            for education_stream in education_streams_list:
                data_view = course_service.get_user_education_progress(_user_id, education_stream.course)
                data_view['education_stream_name'] = education_stream.name

                data_list_view.append(data_view)

        return data_list_view
