from services.education_course_service import EducationCourseService

class EducationListCoursesPageController():

    def get_courses(self):
        """
        Возвращает список курсов

        Returns:
            courses(List): список курсов
        """

        course_service = EducationCourseService()

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
    
    def get_user_view_by_id_and_course_id(self, _user_id, _course_id):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)
            _course_id - Required  : id курса (Int)

        Returns:
            User: пользователь
        """
        course_service = EducationCourseService()

        user = course_service.get_user_by_id_and_course_id(_user_id, _course_id)

        return {"login": user.login, "role": user.role, "active_education_module": user.active_education_module,
                "education_module_expiration_date": str(user.education_module_expiration_date.strftime("%d/%m/%Y"))}
    
    def get_user_view_by_id(self, _user_id):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)

        Returns:
            User: пользователь
        """
        course_service = EducationCourseService()

        user = course_service.get_user_by_id(_user_id)

        return {"login": user.login, "role": user.role, "active_education_module": user.active_education_module,
                "education_module_expiration_date": str(user.education_module_expiration_date.strftime("%d/%m/%Y"))}