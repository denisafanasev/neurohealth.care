from services.course_service import CourseService
from flask import Markup

class EducationMainCourseLessonPageController():

    def get_lesson(self, _id, _id_video):
        course_service = CourseService()

        course = course_service.get_lesson(_id, 1, _id_video)
        if course.lessons.task:
            course.lessons.task = Markup(course.lessons.task)

        if course.lessons.text:
            course.lessons.text = Markup(course.lessons.text)

        lesson = {
            "id": course.id,
            "name": course.name,
            "lesson": {
                "id": course.lessons.id,
                "id_module": course.lessons.id_module,
                "name": course.lessons.name,
                "link": course.lessons.link,
                "materials": course.lessons.materials,
                "text": course.lessons.text,
                "task": course.lessons.task
            }
        }

        return lesson