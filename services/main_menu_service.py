import config


class MainMenuService():

    def init(self):
        """
        Constructor
        @params:
        """

        pass

    def get_data(self):
        """
        Return main menu structure
        @params:
        """

        return config.MAIN_MENU

    def get_active_menu_item_number(self, _endpoint):
        """
        Return a number of _endpoind element in the menu
        @params:
            _endpoind     - Required  : menu element endpoint (Str)
        """

        i = 0
        menu = self.get_data()

        for item in menu:
            if item['endpoint'] == _endpoint:
                try:
                    i = item['value']
                    break
                except Exception as e:
                    pass

        return i
