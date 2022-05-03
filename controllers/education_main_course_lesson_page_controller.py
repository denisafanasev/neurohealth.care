from services.course_service import CourseService
import html
from flask import Markup

class EducationMainCourseLessonPageController():

    def get_lesson(self, _id):
        course_service = CourseService()

        course = course_service.get_lesson(_id)
        if course.lessons.get("task"):
            course.lessons["task"] = Markup(course.lessons["task"])

        if course.lessons.get("text"):
            course.lessons["text"] = Markup(course.lessons["text"])

        lesson = {
            "id": course.id,
            "name": course.name,
            "lesson": course.lessons
        }

        return lesson