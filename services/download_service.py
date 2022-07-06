import os
import config


class DownloadService():
    """
    DownloadService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def get_path_file(self, _name_dataset, _name_file, _id=0):
        """
        Возвращает путь файла

        Args:
            _name_dataset(String): тип директории
            _name_file(String): уникальное название файло
            _id(Int): индентификатор

        Return:
            path_file(String): путь к файлу
        """

        path_file = None

        if _name_dataset == "chat":
            path_file = os.path.abspath(os.path.join(config.DATA_FOLDER, "user_files", f"user_{_name_file.split('_')[0]}", _name_file))

        elif _name_dataset == "course":
            path_file = os.path.abspath(os.path.join(config.DATA_FOLDER, f"course_{_id}", "materials", _name_file))

        return path_file