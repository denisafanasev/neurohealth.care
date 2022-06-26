from services.learning_stream_service import LearningStreamService

class LearningStreamProfilePageController():

    def create_learning_stream(self, _learning_stream):
        """
        Создает обучающий поток

        Args:
            _learning_stream(Dict): обучающий поток
        """

        learning_stream_service = LearningStreamService()

        return learning_stream_service.create_learning_stream(_learning_stream)

    def get_students_list(self):
        """
        Возвращает список пользователей с ролью user

        Returns:
            students_list(List): список пользователей
        """

        learning_stream_service = LearningStreamService()

        students = learning_stream_service.get_students_list()
        students_list = []

        for i_student in students:
            student = {
                'login': i_student.login,
                'name': i_student.name,
            }

            students_list.append(student)

        return students_list

    def get_curators_list(self):
        """
        Возвращает список пользователей с ролью superuser

        Returns:
            curators_list(List): список пользователей
        """

        learning_stream_service = LearningStreamService()

        curators = learning_stream_service.get_curators_list()
        curators_list = []

        for i_curator in curators:
            curator = {
                'login': i_curator.login,
                'name': i_curator.name,
            }

            curators_list.append(curator)

        return curators_list

    def get_courses_list(self):
        """
        Возвращает список курсов

        Returns:
            (List): список курсов
        """

        learning_stream_service = LearningStreamService()

        courses = learning_stream_service.get_courses_list()
        courses_list = []

        for i_course in courses:
            course = {
                'id': i_course.id,
                "name": i_course.name
            }

            courses_list.append(course)

        return courses_list

    def get_learning_stream(self, _id):
        """
        Возвращает обучающий поток по id

        Args:
            _id(Int): идентификатор обучающего потока
        """

        learning_stream_service = LearningStreamService()

        learning_stream = learning_stream_service.get_learning_stream(_id)

        if learning_stream is not None:

            learning_stream_view = {
                "id": learning_stream.id,
                "name": learning_stream.name,
                "course": {
                    "id": learning_stream.course.id,
                    "name": learning_stream.course.name
                },
                "date_start": learning_stream.date_start.strftime("%d/%m/%Y"),
                "date_end": learning_stream.date_end.strftime("%d/%m/%Y"),
                "curators_list": learning_stream.curators_list,
                "students_list": learning_stream.students_list,
                "count_curators": len(learning_stream.curators_list),
                "count_students": len(learning_stream.students_list),
                "teacher": learning_stream.teacher,
                "status": learning_stream.status
            }
        else:
            learning_stream_view = {
                "id": 0,
                "name": "Введите название потока..",
                "course": "Выберить курс обучающего потока..",
                "date_start": "Выберите дату начала обучающего потока..",
                "date_end": "Выберите дату окончания обучающего потока..",
                "curators_list": "Выберите кураторов обучающего потока..",
                "students_list": "Выберите учащихся обучающего потока..",
                "teacher": "Выберите преподавателя обучающего потока..",
            }

        return learning_stream_view

    def change_learning_stream(self, _learning_stream, _old_students_list, _old_curators_list):
        """
        Изменяет данные обучающего потока

        Args:
            _learning_stream(Dict): обучающий поток
            _old_students_list(List): предыдущий список студентов
            _old_curators_list(List): предыдющий список кураторов
        """

        learning_stream_service = LearningStreamService()

        return learning_stream_service.change_learning_stream(_learning_stream, _old_students_list, _old_curators_list)