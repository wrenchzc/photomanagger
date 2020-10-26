import os
from sqlalchemy import and_
from photomanager.pmconst import TODO_INX_NAME
from photomanager.imageutils import ImageInfo
from photomanager.db.helper import exif_to_model
from photomanager.db.models import ImageMeta
from photomanager.helper import get_file_md5
from photomanager.db.config import Config


class ImageDBHandler:
    def __init__(self, folder, session, skip_existed):
        """
        :param session: db session
        :param filenames: list of image filenames
        """
        self.session = session
        self.config = Config(self.session)
        self.folder = folder
        self.skip_existed = skip_existed
        self._on_index_image = None

    @property
    def on_index_image(self):
        return self._on_index_image

    @on_index_image.setter
    def on_index_image(self, func_on_index_image):
        assert callable(func_on_index_image)
        self._on_index_image = func_on_index_image

    def do_index(self, filenames):
        cnt = 0
        for inx, filename in enumerate(filenames):
            filename = filename.strip()
            self.index_image(filename)
            cnt += 1
            if self.on_index_image:
                self.on_index_image(inx)

            if inx % 100 == 0:
                self.session.commit()

        self.session.commit()
        return cnt

    def index_image(self, filename):
        folder = os.path.dirname(filename)
        basename = os.path.basename(filename)
        image_meta_existed = self.session.query(ImageMeta).filter(
            and_(ImageMeta.filename == basename, ImageMeta.folder == folder)).first()
        full_file_name = self.folder + '/' + filename

        if image_meta_existed and (self.skip_existed or image_meta_existed.md5 == get_file_md5(full_file_name)):
            return None

        image_info = ImageInfo(full_file_name)
        image_meta_new = exif_to_model(image_info)

        image_meta_new.filename = basename
        image_meta_new.folder = folder

        if image_meta_existed:
            image_meta_new.id = image_meta_existed.id
            image_meta_new.uuid = image_meta_existed.uuid

        self.session.merge(image_meta_new)
        return image_meta_new

    @property
    def todo_index(self):
        value = self.config.get_value(TODO_INX_NAME)
        if value:
            return int(value)
        else:
            return -1

    @todo_index.setter
    def todo_index(self, value):
        assert isinstance(value, int)
        self.config.set_value(TODO_INX_NAME, value)

