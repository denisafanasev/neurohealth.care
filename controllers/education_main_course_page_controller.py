from services.course_service import CourseService

class EducationMainCoursePageController():

    def get_course(self, _id):

        course_service = CourseService()

        courses = course_service.get_course(_id)
        courses_list = []

        for i_course in courses:
            course = {}
            course["id"] = i_course.id
            course["name"] = i_course.name
            lesson_list = []

            for i_lesson in i_course.lessons:
                lesson = {
                    "id": i_lesson.id,
                    "name": i_lesson.name
                }
                lesson_list.append(lesson)

            course["lessons"] = lesson_list

            courses_list.append(course)

        return courses_list

