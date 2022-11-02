from services.education_streams_service import EducationStreamsService


class EducationStreamsPageController():
    """
    Класс страницы со списком обучающих потоков
    """    

    def get_education_streams(self):
        """
        возвращает отформатированный список обучающих потоков

        Returns:
            List: отформатированный список обучающих потоков
        """        

        education_stream_service = EducationStreamsService()

        education_streams = education_stream_service.get_education_streams()

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
