from services.course_service import CourseService
from flask import Markup

class EducationCourseLessonPageController():

    def get_lesson(self, _id, _id_course):
        course_service = CourseService()

        course = course_service.get_lesson(_id, _id_course)
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