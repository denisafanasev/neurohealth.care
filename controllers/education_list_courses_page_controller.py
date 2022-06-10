from services.course_service import CourseService

class EducationListCoursesPageController():

    def get_courses(self):
        """
        Возвращает список курсов

        Returns:
            courses(List): список курсов
        """

        course_service = CourseService()

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
    
    def get_current_user(self):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)

        Returns:
            User: пользователь
        """
        course_service = CourseService()

        user = course_service.get_current_user()

        return {"login": user.login, "role": user.role, "active_education_module": user.active_education_module,
                "education_module_expiration_date": str(user.education_module_expiration_date.strftime("%d/%m/%Y"))}