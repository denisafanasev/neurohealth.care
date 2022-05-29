from services.upload_service import UploadService

class UploadPageController():

    def get_path_file(self, _name_dataset, _name_file, _id):

        upload_service = UploadService()

        return upload_service.get_path_file(_name_dataset, _name_file, _id)