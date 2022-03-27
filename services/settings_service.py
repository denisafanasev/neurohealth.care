from models.setting_manager import SettingManager

class SettingsService():
    """
    SettingsService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

      
    def get_assessments(self, _file_name):

        setting_manager = SettingManager()

        return setting_manager.get_assessments(_file_name)

    def get_age_ranges(self):

        setting_manager = SettingManager()

        return setting_manager.get_age_ranges()

    def overwrite(self, _file_name, _criteria):

        setting_manager = SettingManager()

        return setting_manager.overwrite(_file_name, _criteria)
