from models.homework_manager import HomeworkManager
from services.upload_service import UploadService

class HomeworkService():

    def get_homeworks(self):

        pass

    def save_homework(self, _homework, _login_user, _id_room_chat):

        homework_manager = HomeworkManager()
        upload_service = UploadService()

        homework_files_list = upload_service.upload_files(_homework, _login_user)
        homework = homework_manager.save_homework(homework_files_list, _id_room_chat)

        homework_manager.create_homework_answers(homework.id)
