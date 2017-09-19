import exifread
import hashlib
import os
import uuid

from PIL import Image


class ImageInfo:
    def __init__(self, filename):
        self.tags = TagInfo(filename)
        self.fileinfo = FileInfo(filename)


class TagInfo:
    def _init_props_by_exif_tags(self):
        self.image_width = self._get_tag_item(tags.get("EXIF ExifImageWidth", None))
        self.image_height = self._get_tag_item(tags.get("EXIF ExifImageLength", None))
        self.image_datetime = self._get_tag_item(tags.get("Image DateTime", None))
        self.origin_datetime = self._get_tag_item(tags.get("EXIF DateTimeOriginal", None))
        self.digital_datetime = self._get_tag_item(tags.get("EXIF DateTimeDigitized", None))
        self.camera_brand = self._get_tag_item(tags.get("Image Make", None))
        self.camera_type = self._get_tag_item(tags.get("Image Model", None))
        self.focal_length = self._get_tag_item(tags.get("EXIF FocalLength", None))
        self.flash = self._get_tag_item(tags.get("EXIF Flash", None))
        self.fnumber = self._get_tag_item(tags.get("EXIF FNumber", None))
        self.aperture = self._get_tag_item(tags.get("EXIF ApertureValue", None))
        self.exposure_time = self._get_tag_item(tags.get("EXIF ExposureTime", None))
        self.exposure_bias = self._get_tag_item(tags.get("EXIF ExposureBiasValue", None))
        self.exposure_mode = self._get_tag_item(tags.get("EXIF ExposureMode", None))
        self.ISO_speed_rating = self._get_tag_item(tags.get("EXIF ISOSpeedRatings", None))
        self.white_balance = self._get_tag_item(tags.get("EXIF WhiteBalance", None))

    def _get_tag_item(self, tag):
        if tag:
            values = tag.values
            if isinstance(values, list):
                if isinstance(values[0], exifread.utils.Ratio):
                    return tag.printable
                else:
                    return values[0]
            elif isinstance(values, str) or isinstance(values, unicode):
                return values.strip()
            else:
                return values

    def _init_props_by_pil(self):
        img = Image.open(f)
        self.image_width = img.width
        self.image_height = img.height

    def __init__(self, filename):

        with open(filename) as f:
            tags = exifread.process_file(f)
            self.has_exif = bool(tags)
            if tags:
                _init_props_by_exif_tags()
            else:
                _init_props_by_pil()

    def info(self):
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__'))


class FileInfo:
    @staticmethod
    def _get_file_md5(filename):
        with open(filename) as f:
            m = hashlib.md5()
            m.update(f.read())
            return m.hexdigest()

    def __init__(self, filename):
        self.size = os.path.getsize(filename)
        self.modify_time = os.path.getmtime(filename)
        self.create_time = os.path.getctime(filename)
        self.md5 = self._get_file_md5(filename)
        self.uuid = str(uuid.uuid1())
