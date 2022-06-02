from models.room_chat_manager import RoomChatManager
from services.user_manager_service import UserManagerService
from services.upload_service import UploadService

class RoomChatService():

    def room_chat_entry(self, _id_lesson, _id_course, _login_user, _id_room_chat):

        room_chat_manager = RoomChatManager()
        user_manager_service = UserManagerService()

        user = user_manager_service.get_current_user(_login_user)

        return room_chat_manager.room_chat_entry(_id_lesson, user, _id_course, _id_room_chat)

    def add_message(self, _message, _room_chat_id):

        room_chat_manager = RoomChatManager()
        user_manager_service = UserManagerService()
        upload_service = UploadService()

        _message["name_sender"] = user_manager_service.get_current_user("").login

        if _message['files'][0].filename != "":
            _message["files"] = upload_service.upload_files(_message["files"], _message["name_sender"])
        else:
            _message["files"] = None

        return room_chat_manager.add_message(_message, _room_chat_id)
