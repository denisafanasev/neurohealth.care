from models.room_chat_manager import RoomChatManager
from services import user_manager_service

class RoomChatService():
    """
    RoomChatService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def room_chat_entry(self, _id_lesson=None, _id_course=None, _login_user='', _id_room_chat=None,
                        _id_learning_stream=None, _id_module=None):
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
        """
        Возвращает данные комнаты чата

        Args:
            _id_room_chat(Int): id чата

        Returns:
            RoomChat: чат
        """

        room_chat_manager = RoomChatManager()

        return room_chat_manager.get_room_chat(_id_room_chat)

    def get_current_user(self, _login_user=""):
        """
        Возвращает данные текущего пользователя

        Args:
            _login_user(String): логин пользователя

        Returns:
            user(Dict): данные пользователя
        """

        user_service = user_manager_service.UserManagerService()

        return user_service.get_current_user(_login_user)


