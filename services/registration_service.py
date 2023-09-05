from models.user_manager import UserManager
from models.email_confirmation_manager import EmailConfirmationManager


class RegistrationService():
    """
    Класс реализующий бизнес-логику приложения, связанную с регистрацией нового пользователя
    Возвращает в слой представления объекты в доменной структуре
    Взаимодейтвует с классами слоя моделей передавая им объекты в доменной структуре
    """    
    
    def is_there_users(self):
        """
        Проверяет, есть ли в системе созданные пользователи
        Используется для того что бы определить при входе в систему не нужно ли создавать суперпользователя

        Returns:
            Boolean: True/False в зависимости от того есть в системе пользователи или нет
        """

        user_manager = UserManager()

        if user_manager.is_there_users():
            return True
        
        return False
    
    def create_user(self, _user_data):
        """
        Создает в системе суперпользователя

        Args:
            _user_data(Dict): данные пользователя для создания в системе
        
        Returns:
            user: созданный пользователь
        """

        user_manager = UserManager()

        _user_data['role'] = "user"
        if _user_data['create_superuser']:
            _user_data['role'] = "superuser"

        # создаем запись нового пользователя базе данных пользователей
        user_manager.create_user(_user_data)

        # если пользователь успешно создан, находим нового только что созданного пользователя
        user = user_manager.get_user_by_login(_user_data['login'])
        return user

    def send_confirmation_email(self, _email, _subject, _template):
        """
        Отправляет пользователю письмо подтверждения регистрации

        Args:
            _email (String): email пользователя
            _html (String): текст письма
        """

        email_manager = EmailConfirmationManager()
        email_manager.send_email(_email, _subject, _template)