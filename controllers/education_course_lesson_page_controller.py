from services.course_service import CourseService
from flask import Markup

class EducationCourseLessonPageController():

    def get_lesson(self, _id, _id_course, _id_video=1):
        course_service = CourseService()

        course = course_service.get_lesson(_id, _id_course, _id_video)
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