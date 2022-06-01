import os

from services.room_chat_service import RoomChatService
import config
from services.user_manager_service import UserManagerService


class DownloadService():

    def get_path_file(self, _name_dataset, _name_file, _id=0):

        path_file = None

        if _name_dataset == "chat":

            user_manager_service = UserManagerService()

            user_login = user_manager_service.get_current_user("").login
            # path_file = f"{config.DATA_FOLDER}user_files/user_{user_login}/{_name_file}"
            path_file = os.path.abspath(os.path.join(config.DATA_FOLDER, "user_files", f"user_{_name_file.split('_')[0]}", _name_file))

        elif _name_dataset == "course":

            # path_file = f"{config.DATA_FOLDER}course_{_id}/materials/{_name_file}"
            path_file = os.path.abspath(os.path.join(config.DATA_FOLDER, f"course_{_id}", "materials", _name_file))

        return path_file