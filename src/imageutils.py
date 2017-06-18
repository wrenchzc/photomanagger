import exifread
import hashlib
import os

from PIL import Image


class TagInfo:
    def __init__(self, tags):

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

        self.image_width = _get_tag_item(tags.get("EXIF ExifImageWidth", None))
        self.image_height = _get_tag_item(tags.get("EXIF ExifImageLength", None))
        self.image_datetime = _get_tag_item(tags.get("Image DateTime", None))
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

    def info(self):
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__'))


def get_file_info(filename):
    size = os.path.getsize(filename)
    modify_time = os.path.getmtime(filename)
    create_time = os.path.getctime(filename)
    md5 = get_file_md5(filename)

    return dict(size=size, modify_time=modify_time, create_time=create_time, md5=md5)


def get_image_info(filename):
    with open(filename) as f:
        tags = exifread.process_file(f)
        if tags:
            tag_info = TagInfo(tags)
            image_info = tag_info.info()
        else:
            img = Image.open(f)
            image_info = dict(image_height=img.height, image_width=img.width)

        return image_info


def get_file_md5(filename):
    with open(filename) as f:
        m = hashlib.md5()
        m.update(f.read())
        return m.hexdigest()
