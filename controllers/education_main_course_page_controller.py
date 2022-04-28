from services.course_service import CourseService

class EducationMainCoursePageController():

    def get_courses(self):

        course_service = CourseService()

        courses = course_service.get_courses()
        courses_list = []

        for i_course in courses:
            course = {}

            course["id"] = i_course.id
            course["name"] = i_course.name
            course["lessons"] = i_course.lessons

            courses_list.append(course)

        return courses_list