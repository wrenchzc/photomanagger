from src.imageutils import ImageInfo
from src.db.helper import exif_to_model


def quote_str(s):
    return '"{s}"'.format(s=s)


class ImageDBHandler:
    def __init__(self, session):
        """
        :param session: db session
        :param filenames: list of image filenames
        """
        self.session = session

    def do_index(self, filenames):
        counter = 0
        for filename in filenames:
            self.index_image(filename)
            counter += 1
            if counter % 100 == 0:
                self.commit()

        self.session.commit()

    def index_image(self, filename):
        image_info = ImageInfo(filename)
        image_meta = exif_to_model(image_info)
        self.session.add(image_meta)
        return image_meta

