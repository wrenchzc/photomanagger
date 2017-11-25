from photomanager.pmconst import TODO_INX_NAME
from photomanager.imageutils import ImageInfo
from photomanager.db.helper import exif_to_model
from photomanager.db.models import Option, ImageMeta
from photomanager.helper import get_file_md5


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
        assert callable(func_on_index_image)
        self._on_index_image = func_on_index_image

    def do_index(self, filenames):
        for inx, filename in enumerate(filenames):
            filename = filename.strip()
            self.index_image(filename)
            if self.on_index_image:
                self.on_index_image(inx)

            if inx % 100 == 0:
                self.session.commit()

        self.session.commit()

    def index_image(self, filename):
        image_meta = self.session.query(ImageMeta).filter(ImageMeta.filename == filename).first()
        full_file_name = self.folder + '/' + filename
        if not image_meta or image_meta.md5 != get_file_md5(full_file_name):
            image_info = ImageInfo(full_file_name)
            image_meta = exif_to_model(image_info)
            image_meta.filename = filename
            self.session.add(image_meta)
            return image_meta

    @property
    def todo_index(self):
        value = self.get_option_value(TODO_INX_NAME)
        if value:
            return int(value)
        else:
            return -1

    @todo_index.setter
    def todo_index(self, value):
        assert isinstance(value, int)
        self.set_option_value(TODO_INX_NAME, value)

    def set_option_value(self, name, value):
        option = self.session.query(Option).filter(Option.name == name).first()
        if not option:
            option = Option()
            option.name = name

        option.value = str(value)
        self.session.add(option)
        self.session.commit()

    def get_option_value(self, name):
        option_todo_inx = self.session.query(Option).filter(Option.name == name).first()
        if option_todo_inx:
            return option_todo_inx.value
