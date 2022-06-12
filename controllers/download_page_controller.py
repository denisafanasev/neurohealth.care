from services.download_service import DownloadService

class DownloadPageController():

    def get_path_file(self, _name_dataset, _name_file, _id):
        """
        Возвращает путь файла

        Args:
            _name_dataset(String): тип директории
            _name_file(String): уникальное название файло
            _id(Int): индентификатор

        Return:
            path_file(String): путь к файлу
        """

        download_service = DownloadService()

        return download_service.get_path_file(_name_dataset, _name_file, _id)