from services.learning_stream_service import LearningStreamService


class LearningStreamPageController():

    def get_learning_streams_list(self):

        learning_stream_service = LearningStreamService()

        learning_streams = learning_stream_service.get_learning_streams_list()

        learning_streams_list = []

        for i_learning_stream in learning_streams:

            learning_stream = {
                "id": i_learning_stream.id,
                "name": i_learning_stream.name,
                "course": {
                    "id": i_learning_stream.course.id,
                    "name": i_learning_stream.course.name
                },
                "date_start": i_learning_stream.date_start.strftime("%d/%m/%Y"),
                "date_end": i_learning_stream.date_end.strftime("%d/%m/%Y"),
                "curators_list": i_learning_stream.curators_list,
                "students_list": i_learning_stream.students_list,
                "count_curators": len(i_learning_stream.curators_list),
                "count_students": len(i_learning_stream.students_list),
                "teacher": i_learning_stream.teacher,
                "status": i_learning_stream.status
            }

            learning_streams_list.append(learning_stream)

        return learning_streams_list

    def get_students_list(self):

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
                "date_start": learning_stream.date_start,
                "date_end": learning_stream.date_end,
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