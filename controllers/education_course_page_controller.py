from services.course_service import CourseService
from services.user_profile_service import UserProfileService


class EducationCoursePageController():

    # TODO: надо переименовать, тк тут возвращается список модулей, а не курс
    def get_course_modules(self, _id):

        course_service = CourseService()

        course = course_service.get_course(_id)
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

    def get_current_user(self):

        # TODO: из контроллера можно вызывать только свой сервис, а 
        course_service = CourseService()

        user = course_service.get_current_user()

        return {"login": user.login, "role": user.role, "active_education_module": user.active_education_module,
                "education_module_expiration_date": str(user.education_module_expiration_date.strftime("%d/%m/%Y"))}
    
    def get_course_by_id(self, _id):
        course_service = CourseService()
        course = course_service.get_course_by_id(_id)

        course_formated = {}
        course_formated["id"] = course.id
        course_formated["name"] = course.name
        course_formated["description"] = course.description
        course_formated["type"] = course.type

        return course_formated