import os
import config

from distutils.command.config import config
from data_adapters.data_store import DataStore
from models.course import Course


class EducationCourseManager():
    """
    Класс модели управления курсами
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """
    
    def course_row_to_course(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о уроке в структуру Lesson

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Course: урок
        """

        course = Course(_data_row.doc_id, _data_row["name"], _data_row["description"], _data_row["type"], _data_row["image"])

        return course

    def get_courses(self):
        """
        Возвращает список курсов

        Returns:
            courses(List): список курсов
        """

        data_store = DataStore("courses_list")

        courses_list = data_store.get_rows()
        courses = []

        for i_course in courses_list:
            courses.append(self.course_row_to_course(i_course))

        return courses
    
    def get_course_by_id(self, _id):
        """
        Возвращает курс по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            course(Course): курс
        """

        course = None

        data_store = DataStore("courses_list")
        course_data = data_store.get_row_by_id(_id)
        if course_data is not None:
            course = self.course_row_to_course(course_data)

        return course
