import os

from services.room_chat_service import RoomChatService
import config

class UploadService():

    def get_path_file(self, _name_dataset, _name_file, _id=0):

        path_file = None

        if _name_dataset == "chat":

            room_chat_service = RoomChatService()
            path_file = room_chat_service.get_path_file(_name_file)

        elif _name_dataset == "course":

            path_file = f"{config.DATA_FOLDER}course_{_id}/materials/{_name_file}"

        return path_file