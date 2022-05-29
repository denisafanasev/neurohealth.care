from models.room_chat_manager import RoomChatManager
from services.user_manager_service import UserManagerService

class RoomChatService():

    def room_chat_entry(self, _id_lesson, _id_course, _login_user, _id_room_chat):

        room_chat_manager = RoomChatManager()
        user_manager_service = UserManagerService()

        user = user_manager_service.get_current_user(_login_user)

        return room_chat_manager.room_chat_entry(_id_lesson, user, _id_course, _id_room_chat)

    def add_message(self, _message, _room_chat_id):

        room_chat_manager = RoomChatManager()
        user_manager_service = UserManagerService()

        _message["name_sender"] = user_manager_service.get_current_user("").login

        return room_chat_manager.add_message(_message, _room_chat_id)

    def get_path_file(self, _name_file):

        room_chat_manager = RoomChatManager()
        user_manager_service = UserManagerService()

        user_login = user_manager_service.get_current_user("").login

        return room_chat_manager.get_path_file(user_login, _name_file)
