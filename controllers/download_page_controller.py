from services.download_service import DownloadService

class DownloadPageController():

    def get_path_file(self, _name_dataset, _name_file, _id):

        download_service = DownloadService()

        return download_service.get_path_file(_name_dataset, _name_file, _id)