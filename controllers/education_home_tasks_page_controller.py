from services.homework_service import HomeworkService

class EducationHomeTasksPageController():

    def get_homeworks_list(self):

        homework_service = HomeworkService()

        homework_list = homework_service.get_homeworks_list()
        homework_list_view = []
        for homework in homework_list:
            room_chat = homework_service.get_room_chat(homework.id_room_chat)
            course = homework_service.get_course(room_chat.id_course)
            lesson = homework_service.get_lesson(room_chat.id_lesson, room_chat.id_course)
            # learning_stream = homework_service.get_learning_stream(room_chat.id_learning_stream)
            user = homework_service.get_current_user(room_chat.login_user)

            homework_view = {
                "id": homework.id,
                "user": {
                    "login": user.login,
                    "name": user.name
                },
                "course": {
                    "id": course.id,
                    "name": course.name
                },
                "lesson": {
                    "id": lesson.id,
                    "name": lesson.name
                },
                # "learning_stream": {
                #     "id": learning_stream.id,
                #     "name": learning_stream.name
                # },
                "date_delivery": homework.date_delivery.strftime("%d/%m/%Y"),
                "users_files_list": homework.users_files_list,
                "homework_answer": {
                    "id": homework.homework_answer.id,
                    "answer": homework.homework_answer.answer,
                    "status": homework.homework_answer.status
                }
            }

            homework_list_view.append(homework_view)

        return homework_list_view

    def change_homework_answer(self, _answer, _id_homework_answer):

        homework_service = HomeworkService()

        homework_service.change_homework_answer(_answer, _id_homework_answer)