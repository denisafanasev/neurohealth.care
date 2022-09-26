from datetime import datetime, timedelta
from services.education_stream_service import EducationStreamService

class EducationStreamPageController():
    """
    Класс страницы карточки обучающего потока
    """    

    def get_students_list(self, _user_id):
        """
        Возвращает список пользователей с ролью user

        Returns:
            students_list(List): список пользователей
        """

        education_stream_service = EducationStreamService()

        students = education_stream_service.get_students_list(_user_id)
        students_list = []

        for i_student in students:
            student = {
                'login': i_student.login,
                'name': i_student.name,
            }

            students_list.append(student)

        return students_list

    def get_curators_list(self, _user_id):
        """
        Возвращает отформатированный список пользователей с ролью superuser

        Returns:
            [List]: список пользователей
        """

        education_stream_service = EducationStreamService()

        curators = education_stream_service.get_curators_list(_user_id)
        curators_list = []

        for i_curator in curators:
            curator = {
                'login': i_curator.login,
                'name': i_curator.name,
            }

            curators_list.append(curator)

        return curators_list

    def get_courses_list(self, _user_id):
        """
        Возвращает список курсов

        Returns:
            (List): список курсов
        """

        education_stream_service = EducationStreamService()

        courses = education_stream_service.get_courses_list(_user_id)
        courses_list = []

        for i_course in courses:
            course = {
                'id': i_course.id,
                "name": i_course.name
            }

            courses_list.append(course)

        return courses_list

    def get_education_stream(self, _id):
        """
        Возвращает представление обучающего потока по id

        Args:
            _id(Int): идентификатор обучающего потока
        """

        education_stream_service = EducationStreamService()

        education_stream = education_stream_service.get_education_stream(_id)

        if education_stream is not None:

            education_stream_view = {
                "id": education_stream.id,
                "name": education_stream.name,
                "course": {
                    "id": education_stream.course.id,
                    "name": education_stream.course.name
                },
                "date_start": education_stream.date_start.strftime("%d/%m/%Y"),
                "date_end": education_stream.date_end.strftime("%d/%m/%Y"),
                "curators_list": education_stream.curators_list,
                "students_list": education_stream.students_list,
                "count_curators": len(education_stream.curators_list),
                "count_students": len(education_stream.students_list),
                "teacher": education_stream.teacher,
                "status": education_stream.status
            }
        else:
            education_stream_view = {
                "id": 0,
                "name": "Введите название потока..",
                "course": "Выберить курс обучающего потока..",
                "date_start": datetime.today().strftime("%d/%m/%Y"),
                "date_end": (datetime.today() + timedelta(days=60)).strftime("%d/%m/%Y"),
                "curators_list": "Выберите кураторов обучающего потока..",
                "students_list": "Выберите учащихся обучающего потока..",
                "teacher": "Выберите преподавателя обучающего потока..",
            }

        return education_stream_view
    
    def create_education_stream(self, _education_stream):
        """
        Создает обучающий поток

        Args:
            _education_stream(Dict): обучающий поток

        Returns:
            id(Int): идентификатор обучающего потока
        """
        education_stream_manager = EducationStreamService()

        education_stream_manager.create_education_stream(_education_stream)


    def change_education_stream(self, _education_stream, _old_students_list, _old_curators_list):
        """
        Изменяет данные обучающего потока

        Args:
            _education_stream(Dict): обновленные атрибуты обучающего потока
        """

        education_stream_service = EducationStreamService()

        education_stream_service.change_education_stream(_education_stream)

        _education_stream['course'] = _education_stream.pop("id_course")