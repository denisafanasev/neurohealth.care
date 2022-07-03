from services.education_stream_service import EducationStreamService


class EducationStreamPageController():

    def get_education_streams_list(self):

        education_stream_service = EducationStreamService()

        education_streams = education_stream_service.get_education_streams_list()

        education_streams_list = []

        for i_education_stream in education_streams:

            education_stream = {
                "id": i_education_stream.id,
                "name": i_education_stream.name,
                "course": {
                    "id": i_education_stream.course.id,
                    "name": i_education_stream.course.name
                },
                "date_start": i_education_stream.date_start.strftime("%d/%m/%Y"),
                "date_end": i_education_stream.date_end.strftime("%d/%m/%Y"),
                "curators_list": i_education_stream.curators_list,
                "students_list": i_education_stream.students_list,
                "count_curators": len(i_education_stream.curators_list),
                "count_students": len(i_education_stream.students_list),
                "teacher": i_education_stream.teacher,
                "status": i_education_stream.status
            }

            education_streams_list.append(education_stream)

        return education_streams_list

    def get_students_list(self):

        education_stream_service = EducationStreamService()

        students = education_stream_service.get_students_list()
        students_list = []

        for i_student in students:
            student = {
                'login': i_student.login,
                'name': i_student.name,
            }

            students_list.append(student)

        return students_list

    def get_curators_list(self):

        education_stream_service = EducationStreamService()

        curators = education_stream_service.get_curators_list()
        curators_list = []

        for i_curator in curators:
            curator = {
                'login': i_curator.login,
                'name': i_curator.name,
            }

            curators_list.append(curator)

        return curators_list

    def get_courses_list(self):

        education_stream_service = EducationStreamService()

        courses = education_stream_service.get_courses_list()
        courses_list = []

        for i_course in courses:
            course = {
                'id': i_course.id,
                "name": i_course.name
            }

            courses_list.append(course)

        return courses_list

    def get_education_stream(self, _id):

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
                "date_start": education_stream.date_start,
                "date_end": education_stream.date_end,
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
                "date_start": "Выберите дату начала обучающего потока..",
                "date_end": "Выберите дату окончания обучающего потока..",
                "curators_list": "Выберите кураторов обучающего потока..",
                "students_list": "Выберите учащихся обучающего потока..",
                "teacher": "Выберите преподавателя обучающего потока..",
            }

        return education_stream_view