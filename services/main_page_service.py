from models.user_manager import UserManager
class MainPageService():
    """
    MainPageService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """
    
    def init(self):
        pass

    def get_data(self):
        return "Data"

    def get_user_by_id(self, _user_id):
        """
        Фукция возвращает пользователя по его id

        Args:
            _user_id (_type_): id пользователя

        Returns:
            User: пользователь
        """        

        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)

        return user