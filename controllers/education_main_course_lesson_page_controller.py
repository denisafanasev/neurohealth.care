from services.course_service import CourseService

class EducationMainCourseLessonPageController():

    def get_lesson(self, _id):
        course_service = CourseService()

        course = course_service.get_lesson(_id)

        lesson = {
            "id": course.id,
            "name": course.name,
            "lesson": course.lessons
        }

        return lesson