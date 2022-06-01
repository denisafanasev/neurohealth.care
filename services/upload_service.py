from werkzeug.utils import secure_filename
import os
import config

class UploadService():

    def upload_files(self, _files_list, _user_login):

        files = []
        for i_file in _files_list:

            user_dir = "user_{}".format(_user_login)
            if not "user_files" in os.listdir(config.DATA_FOLDER):
                os.mkdir(config.DATA_FOLDER + "user_files")

            path = config.DATA_FOLDER + "user_files/" + user_dir

            if not user_dir in os.listdir(config.DATA_FOLDER + "user_files"):
                os.mkdir(path)
                amount = 0
            else:
                amount = len(os.listdir(path))

            type_file = i_file.content_type.split("/")[-1]
            user_file_unique = "{login}_file_{num}.{type}".format(num=amount + 1, type=type_file, login=_user_login)
            name_file_user = i_file.filename

            if name_file_user[0] == '.':
                name_file_user = secure_filename(name_file_user)

            files.append({"name_file_unique": user_file_unique, "name_file_user": name_file_user, "path": path})
            i_file.save(os.path.join(path, user_file_unique))

        return files