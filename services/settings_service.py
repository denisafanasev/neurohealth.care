from models.setting_manager import SettingManager

class SettingsService():
    """
    SettingsService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_assessments(self):

        setting_manager = SettingManager()

        return setting_manager.get_assessments()
