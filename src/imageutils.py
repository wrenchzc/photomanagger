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
    def __init__(self, filename):

        def _get_tag_item(tag):
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

        def _init_props_by_exif_tags():
            self.image_width = _get_tag_item(tags.get("EXIF ExifImageWidth", None))
            self.image_height = _get_tag_item(tags.get("EXIF ExifImageLength", None))
            self.image_datetime = _get_tag_item(tags.get("Image DateTime", None))
            self.origin_datetime = _get_tag_item(tags.get("EXIF DateTimeOriginal", None))
            self.digital_datetime = _get_tag_item(tags.get("EXIF DateTimeDigitized", None))
            self.camera_brand = _get_tag_item(tags.get("Image Make", None))
            self.camera_type = _get_tag_item(tags.get("Image Model", None))
            self.focal_length = _get_tag_item(tags.get("EXIF FocalLength", None))
            self.flash = _get_tag_item(tags.get("EXIF Flash", None))
            self.fnumber = _get_tag_item(tags.get("EXIF FNumber", None))
            self.aperture = _get_tag_item(tags.get("EXIF ApertureValue", None))
            self.exposure_time = _get_tag_item(tags.get("EXIF ExposureTime", None))
            self.exposure_bias = _get_tag_item(tags.get("EXIF ExposureBiasValue", None))
            self.exposure_mode = _get_tag_item(tags.get("EXIF ExposureMode", None))
            self.ISO_speed_rating = _get_tag_item(tags.get("EXIF ISOSpeedRatings", None))
            self.white_balance = _get_tag_item(tags.get("EXIF WhiteBalance", None))

        def _init_props_by_pil():
            img = Image.open(f)
            self.image_width = img.width
            self.image_height = img.height

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
    def __init__(self, filename):
        self.size = os.path.getsize(filename)
        self.modify_time = os.path.getmtime(filename)
        self.create_time = os.path.getctime(filename)
        self.md5 = get_file_md5(filename)
        self.uuid = str(uuid.uuid1())


def get_file_md5(filename):
    with open(filename) as f:
        m = hashlib.md5()
        m.update(f.read())
        return m.hexdigest()
