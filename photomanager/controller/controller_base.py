class UIControllerBase(object):

    def __before_show__(self):
        pass

    def __init__(self, base_folder: str, db_session, ui_data: object):
        self.base_folder = base_folder
        self.db_session = db_session
        self.ui_data = ui_data
        self.__before_show__()
