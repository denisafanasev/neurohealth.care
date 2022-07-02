from flask import Markup

from services.room_chat_service import RoomChatService

class EducationChatPageController():
    """
    EducationChatPageController - класс контроллера представления чата с пользователями, реализующий логику взаимодействия приложения с пользователем
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответствующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    def room_chat_entry(self, _id_room_chat):
        """
        Подключает пользователя к чату

        Args:
            _id_room_chat(Int): индентификатор чата

        Returns:
            Dict: чат
        """

        room_chat_service = RoomChatService()

        room_chat = room_chat_service.room_chat_entry(_id_room_chat=_id_room_chat)

        room_chat_view = {
            "id": room_chat.id,
            "message": None
        }

        if room_chat.message is not None:
            message_list = []
            for i_message in room_chat.message:
                message = {
                    "id": i_message.id,
                    "text": Markup(i_message.text),
                    "name_sender": i_message.name_sender,
                    "date_send": i_message.date_send.strftime("%d/%m/%Y")
                }

                message_list.append(message)

            room_chat_view["message"] = message_list

        return room_chat_view

    def add_message(self, _message, _room_chat_id):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _room_chat_id(Int): индентификатор чата
        """

        room_chat_service = RoomChatService()

        return room_chat_service.add_message(_message, _room_chat_id)

    def get_current_user(self):
        """
        Возвращает данные текущего пользователя

        Returns:
            user(Dict): данные пользователя
        """

        room_chat_service = RoomChatService()

        user = room_chat_service.get_current_user()
        user_view = {
            "login": user.login,
            "role": user.role,
            "active_education_module": user.active_education_module,
            "education_module_expiration_date": user.education_module_expiration_date.strftime("%d/%m/%Y"),
            "learning_stream": {}
        }


        return user_view