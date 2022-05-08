from services.course_service import CourseService
from flask import Markup

class EducationMainCourseLessonPageController():

    def get_lesson(self, _id):
        course_service = CourseService()

        course = course_service.get_lesson(_id, 1)
        if course.lessons.task:
            course.lessons.task = Markup(course.lessons.task)

        if course.lessons.text:
            course.lessons.text = Markup(course.lessons.text)

        lesson = {
            "id": course.id,
            "name": course.name,
            "lesson": course.lessons
        }

        return lesson