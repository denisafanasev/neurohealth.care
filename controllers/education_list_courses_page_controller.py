from services.course_service import CourseService

class EducationListCoursesPageController():

    def get_courses(self):

        course_service = CourseService()

        courses = course_service.get_courses()
        courses_list = []

        for i_course in courses:

            course = {
                "id": i_course.id,
                "name": i_course.name,
                "description": i_course.description,
                "image": i_course.image
            }
            courses_list.append(course)

        return courses_list