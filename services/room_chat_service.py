from models.room_chat_manager import RoomChatManager
from services import user_manager_service

class RoomChatService():
    """
    RoomChatService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def room_chat_entry(self, _id_lesson, _id_course, _login_user, _id_room_chat, _id_learning_stream, _id_module):
        """
        Подключает пользователя к чату

        Args:
            _id_lesson(Int): индентификатор урока
            _login_user(User): логин пользователя
            _id_course(Int): индентификатор курса
            _id_room_chat(Int): индентификатор чата

        Returns:
            RoomChat: чат
        """

        room_chat_manager = RoomChatManager()
        user_service = user_manager_service.UserManagerService()

        user = user_service.get_current_user(_login_user)

        return room_chat_manager.room_chat_entry(_id_lesson, user, _id_course, _id_room_chat, _id_learning_stream,
                                                 _id_module)

    def add_message(self, _message, _room_chat_id):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _room_chat_id(Int): индентификатор чата
        """

        room_chat_manager = RoomChatManager()
        user_service = user_manager_service.UserManagerService()

        _message["name_sender"] = user_service.get_current_user("").login

        return room_chat_manager.add_message(_message, _room_chat_id)

    def get_room_chat(self, _id_room_chat):

        room_chat_manager = RoomChatManager()

        return room_chat_manager.get_room_chat(_id_room_chat)



