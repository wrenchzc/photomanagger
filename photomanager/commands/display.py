import typing
from photomanager.commands.base import Command
from photomanager.lib.filter import FiltersParser
from photomanager.db.models import ImageMeta
from photomanager.ui.window_disp_image import WindowDispImage
from photomanager.ui.qt_app import qt_app
from photomanager.utils.logger import logger


class CommandList(Command):
    def __init__(self, folder, params):
        Command.__init__(self, folder, params)
        self.filters = self.params['filters']

    def get_filter_images(self) -> typing.List[typing.Dict] :
        filter_parser = FiltersParser(self.filters)
        filter_expression = filter_parser.parse()
        qry = self.db_session.query(ImageMeta).filter(filter_expression)
        results = qry.all()

        disp_imags:typing.List[typing.Dict] = []
        for result in results:
            disp_imags.append(result.get_dict_info())
        return disp_imags

    def show(self, image_infos):
        w_file_dup = WindowDispImage(self.folder, self.db_session, image_infos)
        w_file_dup.show()
        qt_app.exec_()

    def do(self):
        disp_images = self.get_filter_images()
        if disp_images:
            self.show(disp_images)
        else:
            logger.info(f"no images match for filter {self.filters}")






