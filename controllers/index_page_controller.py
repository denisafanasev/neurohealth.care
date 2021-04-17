import utils.ada as ada
from services.index_service import IndexService


class IndexPageController():

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_data(self):
        index_service = IndexService()
        return index_service.get_data()
