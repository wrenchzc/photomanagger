import os
from src.imageutils import ImageInfo
from src.db.helper import exif_to_model


def quote_str(s):
    return '"{s}"'.format(s=s)


class ImageDBHandler:
    def __init__(self, folder, session):
        """
        :param session: db session
        :param filenames: list of image filenames
        """
        self.session = session
        self.folder = folder
        self._on_index_image = None

    @property
    def on_index_image(self):
        return self._on_index_image

    @on_index_image.setter
    def on_index_image(self, func_on_index_image):
        assert isinstance(func_on_index_image, function)
        self._on_index_image = func_on_index_image

    def do_index(self, filenames):
        for inx, filename in enumerate(filenames):
            self.index_image(self.folder + os.path.sep + filename)
            if self.on_index_image:
                self.on_index_image(inx)

            if inx % 100 == 0:
                self.session.commit()

        self.session.commit()

    def index_image(self, filename):
        image_info = ImageInfo(filename)
        image_meta = exif_to_model(image_info)
        self.session.add(image_meta)
        return image_meta
